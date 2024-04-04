import sqlite3


def save_plan(user_id, day_of_week, plan):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weekly_schedule (user_id, day_of_week, plan) VALUES (?, ?, ?)",
                   (user_id, day_of_week, plan))
    conn.commit()
    conn.close()


def get_day_of_week(user_id, day_of_week):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute("SELECT plan FROM weekly_schedule WHERE user_id=? AND day_of_week=?", (user_id, day_of_week))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def update_plan(user_id, plan, day):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE weekly_schedule SET plan=? WHERE user_id=? AND day_of_week=?", (plan, user_id, day))
    conn.commit()
    conn.close()


def delete_plan_in_day(user_id, day):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weekly_schedule WHERE user_id=? AND day_of_week=?", (user_id, day))
    conn.commit()
    conn.close()


def add_cpfc(user_id, protein, fat, carbohydrate, calories, gram):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT protein, fat, carbohydrate, calories FROM user_cpfc WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is not None:  # Если за сегодня добавлял, рассчитывает кБЖУ и вносит в бд
        a = int(gram) / 100
        new_protein = result[0] + protein * a
        new_fat = result[1] + fat * a
        new_carbohydrate = result[2] + carbohydrate * a
        new_calories = result[3] + calories * a

        cursor.execute("UPDATE user_cpfc SET protein=?, fat=?, carbohydrate=?, calories=? WHERE user_id=?",
                       (new_protein, new_fat, new_carbohydrate, new_calories, user_id))
        conn.commit()
        conn.close()
    else:  # Если нет, то добавляет за сегодня
        a = int(gram) / 100
        new_protein = int(protein) * a
        new_fat = int(fat) * a
        new_carbohydrate = int(carbohydrate) * a
        new_calories = int(calories) * a
        cursor.execute("INSERT INTO user_cpfc (user_id, protein, fat, carbohydrate, calories) VALUES (?, ?, ?, ?, ?)",
                       (user_id, new_protein, new_fat, new_carbohydrate, new_calories))
        conn.commit()
        conn.close()


def insert_cpfc_need(user_id, protein, fat, carbohydrate, calories):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_cpfc_need (user_id, protein_need, fat_need, carbohydrate_need, calories_need)"
        " VALUES (?, ?, ?, ?, ?)",
        (user_id, protein, fat, carbohydrate, calories))
    conn.commit()
    conn.close()


def get_data_cpfc(user_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT protein, fat, carbohydrate, calories FROM user_cpfc WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return [a if a is not None else 0 for a in result]
    else:
        return [0, 0, 0, 0]


def get_data_need_cpfc(user_id):  # Выводит сколько необходимо кБЖУ
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT protein_need, fat_need, carbohydrate_need, calories_need FROM user_cpfc_need WHERE user_id=?",
        (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def chek_need_cpfc(user_id):  # Проверяет есть ли юзер в базе
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_cpfc_need WHERE user_id=?", (user_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return True if result > 0 else False


def find_food(food_name):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food WHERE name=?", (food_name,))

    product = cursor.fetchone()

    conn.close()
    return product


def insert_food(name, protein, fat, carbohydrate, calories):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM food WHERE name = ?", (name,))
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            "INSERT INTO food (name, protein, fat, carbohydrate, calories) VALUES (?, ?, ?, ?, ?)",
            (name, protein, fat, carbohydrate, calories))
        conn.commit()
        conn.close()
    else:
        conn.close()


def delete_cpfc(user_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM user_cpfc WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def add_user(user_id, gender, preference):
    conn = sqlite3.connect("schedule.db")

    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, gender, preference) VALUES (?, ?, ?)", (user_id, gender, preference))
    conn.commit()
    conn.close()


def insert_partner(partner, user_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET partner_id = ? WHERE user_id = ?", (partner, user_id))
    conn.commit()
    conn.close()


def find_candidates(user_gender, preference):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE gender=? AND preference=? AND partner_id IS NULL",
                   (preference, user_gender))
    result = [row[0] for row in cursor.fetchall()]
    print(result)
    conn.close()
    return result


print(find_candidates("Man", "Women"))
print(find_candidates("Women", "Man"))


def delete_user(user_id):
    conn = sqlite3.connect("schedule.db")

    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()


def find_admin(user_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE user_id=?", (user_id,))
    admin = [row[0] for row in cursor.fetchall()]

    conn.close()
    return admin

# Таблица расписаний юзера
# weekly_schedule(название таблицы)
# user_id
# day_of_week
# plan

# Таблица кБЖУ (общая)
# food(название таблицы)
# id
# name
# protein
# fat
# carbohydrate
# calories

# Таблица кБЖУ юзера
# user_cpfc(название таблицы)
# user_id
# protein
# fat
# carbohydrate
# calories
# protein_need
# fat_need
# carbohydrate_need
# calories_need

# users
# user_ip
# gender
# preference
