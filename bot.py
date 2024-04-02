import telebot
from telebot import types
import database
import util

Token = "6609998211:AAG1inKSYLKS4P4pN5Lmc2XuTxaSjOXmypk"
bot = telebot.TeleBot(Token)

admin = 1395590859


@bot.message_handler(commands=['start'])
def start(message):
    database.delete_user(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Расписание", callback_data="schedule")
    btn2 = types.InlineKeyboardButton("кБЖУ", callback_data="CPFC")
    btn5 = types.InlineKeyboardButton("Общение", callback_data="communication")
    btn3 = types.InlineKeyboardButton("Музыка", callback_data="Music")
    btn4 = types.InlineKeyboardButton("Магазин", url="https://t.me/FitFocusBot/FitFocus")
    markup.add(btn1)
    markup.add(btn5, btn2)
    markup.add(btn4, btn3)
    bot.send_message(message.chat.id, """🚀 Добро пожаловать! 🎉 Начнем ваш фитнес-путешествие с впечатляющего старта! 
    Я ваш верный помощник в достижении ваших целей здоровья и фитнеса. 💪🏋️‍♂️ 
    Приготовьтесь к увлекательному путешествию! 
    Нажмите на одну из кнопок ниже, чтобы начать:

💼 Расписание: Создайте свое персональное расписание тренировок.
🍏 кБЖУ: Узнайте свои калории, белки, жиры и углеводы для правильного питания.
💬 Общение:Здесь вы можете поделиться своим опытом, задать вопросы или просто поболтать
🎵 Музыка: Наслаждайтесь музыкой во время тренировок.
🛒 Магазин: Приобретайте необходимое оборудование и аксессуары для вашего фитнеса.
Выберите интересующую вас опцию и давайте начнем! 🌟""", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == "schedule")
def schedule(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Понедельник", callback_data="Monday")
    btn2 = types.InlineKeyboardButton("Вторник", callback_data="Tuesday")
    btn3 = types.InlineKeyboardButton("Среда", callback_data="Wednesday")
    btn4 = types.InlineKeyboardButton("Четверг", callback_data="Thursday")
    btn5 = types.InlineKeyboardButton("Пятница", callback_data="Friday")
    btn6 = types.InlineKeyboardButton("Суббота", callback_data="Saturday")
    btn7 = types.InlineKeyboardButton("Воскресенье", callback_data="Sunday")
    markup.add(btn1, btn2, btn3)
    markup.add(btn4, btn5, btn6)
    markup.add(btn7)
    bot.send_message(message.message.chat.id,
                     "Выберите день недели, чтобы составить план на неделю вперед. "
                     "Станьте организованным и дисциплинированным с нашим помощником. 💪📝 "
                     "Нажмите на одну из кнопок ниже, чтобы начать:",
                     reply_markup=markup)


@bot.callback_query_handler(
    func=lambda day_week: day_week.data in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
                                            "Sunday"])
def send(message):
    day = message.data
    day_in_russ = {"Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда", "Thursday": "Четверг",
                   "Friday": "Пятница", "Saturday": "Суббота", "Sunday": "Воскресенье"}
    user_id = message.message.chat.id
    plans = database.get_day_of_week(user_id, day)
    if plans:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Изменить", callback_data="Change")
        btn2 = types.InlineKeyboardButton("Удалить", callback_data="Delete")
        markup.add(btn1, btn2)
        bot.send_message(user_id,
                         f"🚀 Посмотрите, что запланировано на этот день и приступайте к действию! 🌟"
                         f" Нажмите кнопку 'Изменить', чтобы внести изменения в планы"
                         f"\n🎯'Удалить' если хотите удалить какие-то пункты."
                         f"\nВаше расписание:\n{plans}",
                         reply_markup=markup)

    else:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Добавить", callback_data="Add_plan")
        markup.add(btn1)
        bot.send_message(user_id,
                         f"🚫 Ваш план на {day_in_russ[day]} пока пуст! 😔 Но не расстраивайтесь! "
                         f"Есть прекрасная возможность добавить новые задачи и цели! 📝"
                         f"Нажмите кнопку 'Добавить' ниже, чтобы начать заполнять свой план на этот день."
                         f"Сделайте свой день полезным и продуктивным!💪📅", reply_markup=markup)

    @bot.callback_query_handler(func=lambda change: change.data in ["Change", "Delete", "Add_plan"])
    def change_delete_add(update):
        if update.data == "Change":
            bot.send_message(user_id,
                             "🔄 Пришло время внести изменения в ваше расписание! 📅🔧"
                             " Давайте сделаем ваш день еще более продуктивным и интересным! "
                             "Ваши возможности безграничны! 💪🌟")

            @bot.message_handler(content_types=['text'])
            def change_schedule(message1):
                database.update_plan(user_id, message1.text, day)
                bot.reply_to(message1, "✅ План успешно сохранен! Давайте вперед к достижению ваших целей! 💪")

        elif update.data == "Delete":
            database.delete_plan_in_day(user_id, day)
            bot.reply_to(update.message,
                         "🗑️ План успешно удален! Не беспокойтесь,"
                         " всегда есть возможность создать новые и еще более удивительные планы! ")

        elif update.data == "Add_plan":
            bot.send_message(user_id, "📝 Добавьте новый план и сделайте этот день незабываемым!💡")

            @bot.message_handler(func=lambda msg: True)
            def add_schedule(message1):
                database.save_plan(user_id, day, message1.text)
                bot.reply_to(message1,
                             "🎉 План успешно добавлен! Теперь ваш день станет еще более интересным и продуктивным!")


@bot.callback_query_handler(func=lambda cpfc: cpfc.data == "CPFC")
def gender(message):
    user_id = message.message.chat.id
    if database.chek_need_cpfc(user_id) is False:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Я парень", callback_data="boy")
        btn2 = types.InlineKeyboardButton("Я девушка", callback_data="girl")
        markup.add(btn1, btn2)
        bot.send_message(user_id, "fed ", reply_markup=markup)
    else:
        cpfc_need = database.get_data_need_cpfc(user_id)
        cpfc = util.left_cpfc(database.get_data_need_cpfc(user_id), database.get_data_cpfc(user_id))
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Добавить", callback_data="cpfc_add")
        btn2 = types.InlineKeyboardButton("Обновить", callback_data="update_cpfc")
        markup.add(btn1, btn2)
        bot.send_message(user_id, f"""Ваше необходимое КБЖУ:
Белок: {int(cpfc_need[0])}
Жиры: {int(cpfc_need[1])}
Углеводы: {int(cpfc_need[2])}
Калории: {int(cpfc_need[3])}

Cегодня вам необходимо употребить:
Белок: {cpfc[0]}
Жир: {cpfc[1]}
Углевод: {cpfc[2]}
Калории: {cpfc[3]}
Нажмите 'Добавить' что бы добавить кБЖУ на сегодня
Нажмите 'Обновить' что бы обновить на сегодняшний день """, reply_markup=markup)


@bot.callback_query_handler(func=lambda gender_user: gender_user.data in ["boy", "girl", "cpfc_add", "update_cpfc"])
def gender_u(message):
    global gen
    user_id = message.message.chat.id
    if message.data == "boy" or message.data == "girl":
        gen = message.data
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Для похудения", callback_data="defecate")
        btn2 = types.InlineKeyboardButton("Для поддержания", callback_data="saving")
        btn3 = types.InlineKeyboardButton("Для увеличения", callback_data="surplus")
        markup.add(btn1, btn2, btn3)
        bot.send_message(user_id,
                         "Независимо от того, стремитесь ли вы к стройности, "
                         "поддержанию формы или набору мышечной массы, у нас есть оптимальный план для вас! 🏋️‍♂️💪 "
                         "Просто выберите свою цель ниже, и мы сделаем все возможное, "
                         "чтобы помочь вам достичь желаемых результатов! 🚀💬",
                         reply_markup=markup)
    else:
        if message.data == "update_cpfc":
            database.delete_cpfc(user_id)
            bot.send_message(user_id, "Успешно обновлено✅")
        elif message.data == "cpfc_add":
            bot.send_message(user_id,
                             "🍴 Давайте добавим продукт в список! Введите название продукта и его вес в граммах."
                             "\nПример: сникерс 50")

            @bot.message_handler(func=lambda msg: True)
            def add_cpfc(message1):
                product = message1.text.lower().split()
                a, b = util.product(product)
                list_food = database.find_food(a[0])
                if b:
                    if list_food is not None:
                        database.add_cpfc(user_id, list_food[2], list_food[3], list_food[4], list_food[5], b[0])
                        bot.reply_to(message1, "Хорошо,записал✅\nНажмите на /start что бы перейти в главное меню")
                    else:
                        bot.reply_to(message1, f"К сожалению, в базе данных не найдено {product[0]}.\n"
                                               f"Но вы можете добавить ваш продукт в базу данных.\n"
                                               f"Напишите кБЖУ продукта в данном виде (обычно эта информация хранится "
                                               f"на этикетке продукта):\n"
                                               f"Пример: Куриная грудка (филе) 23.6 1.9 0.4 113-(Название) Б Ж У К \n"
                                               f"Если на вашем продукте нет этикетки, можете поискать в интернете \n"
                                               f"Название продукта кБЖУ в 100 граммах")
                        bot.register_next_step_handler(message1, add_product)

                else:
                    bot.send_message(user_id, "Введите корректно... \nПример:Сникерс 100")

            def add_product(message1):
                need = message1.text.lower().split()
                name, cpfc = util.product(need)
                if isinstance(name, str) and all(isinstance(numbers, int) for numbers in cpfc):
                    database.insert_food(name[0], *cpfc)
                    bot.send_message(user_id, "Спасибо за понимание. Ваш продукт успешно загружен в базу✅")
                else:
                    bot.send_message(user_id,
                                     f"Возникла ошибка... Введите еще раз данные.\n"
                                     f"Пример: Куриная грудка (филе) 23.6 1.9 0.4 113-(Название) Б Ж У К")


@bot.callback_query_handler(func=lambda weight: weight.data in ["defecate", "saving", "surplus"])
def activ(bob):
    global purpose
    purpose = bob.data
    markup2 = types.InlineKeyboardMarkup()
    btn12 = types.InlineKeyboardButton("Низкий уровень", callback_data="few")
    btn22 = types.InlineKeyboardButton("Средний уровень ", callback_data="normal")
    btn32 = types.InlineKeyboardButton("Высокий уровень", callback_data="high")
    markup2.add(btn12, btn22, btn32)
    bot.send_message(bob.message.chat.id, """" Выберите вашу дневную активность:
Низкий уровень активности:
Сидячий образ жизни, мало физической активности.🖥
Работа в офисе, мало или отсутствие физических упражнений.🏦
Минимальное количество ежедневных прогулок или занятий спортом.🏡

Средний уровень активности:
Умеренная физическая активность, такая как занятия спортом 2-3 раза в неделю🚵🏻
Ежедневные прогулки или активная деятельность в течение дня🏌🏻
Работа, требующая некоторого физического напряжения, но без интенсивных физических упражнений🚗

Высокий уровень активности:
Интенсивные тренировки или занятия спортом 4-6 раз в неделю.🏋
Физическая работа или активный образ жизни, требующие значительного физического усилия🏊
Высокий уровень ежедневной активности и движения⛹""", reply_markup=markup2)


@bot.callback_query_handler(func=lambda active: active.data in ["few", "normal", "high"])
def formula(jo):
    active = jo.data
    bot.send_message(jo.message.chat.id,
                     f"📊 Давайте подберем идеальную программу для вас! 🏃‍♂️💨 "
                     f"Выберите ваш уровень активности: низкий, средний или высокий, и мы приступим к расчетам! 💪🔢 "
                     f"После выбора уровня активности, пожалуйста, напишите свой рост, вес и возраст в формате: "
                     f"'Рост Вес Возраст'. Например: 175 70 20. "
                     f"Давайте вместе создадим вашу идеальную тренировочную программу! 💬📏")

    @bot.message_handler(func=lambda msg: True)
    def h_w_o(message):
        try:
            need = message.text.split()
            calories = util.calories(int(need[0]), int(need[1]), int(need[2]), gen, active, purpose)
            protein_need = util.protein_and_fat(calories)
            fat_need = util.protein_and_fat(calories)
            carbohydrate_need = util.carbohydrate(calories)
            database.insert_cpfc_need(jo.message.chat.id, protein_need, fat_need, carbohydrate_need, calories)
            bot.send_message(jo.message.chat.id, "Ваше необходимое кБЖУ записано✅")
        except ValueError:
            bot.send_message(jo.message.chat.id, f"Возникла ошибка... Введите еще раз свои данные\nпример: 175 70 20")


@bot.callback_query_handler(func=lambda music: music.data == "Music")
def url_music(user):
    user_id = user.message.chat.id
    bot.send_message(user_id, "Привет! Чтобы получить ссылку на скачивание музыки, просто введи ее название,"
                              " и я найду для тебя самый подходящий трек! 🎶")

    @bot.message_handler(content_types=['text'])
    def get_music_url(message):
        bot.reply_to(message, util.send_music(message.text))


@bot.callback_query_handler(func=lambda talk: talk.data == "communication")
def communication(button):
    user_id = button.message.chat.id
    database.delete_user(user_id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Парень", callback_data="Man")
    btn2 = types.InlineKeyboardButton("Девушка", callback_data="Women")
    markup.add(btn1, btn2)
    bot.send_message(user_id, "Привет! Чтобы начать общение, выбери свой пол: ", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ["Man", "Women"])
def choice_partner(message):
    global user_gender
    user_gender = message.data
    user_id = message.message.chat.id
    markup_find = types.InlineKeyboardMarkup()
    btn3 = types.InlineKeyboardButton("Парень", callback_data="find_Man")
    btn4 = types.InlineKeyboardButton("Девушка", callback_data="find_Women")
    markup_find.add(btn3, btn4)
    bot.edit_message_text(chat_id=user_id, message_id=message.message.message_id,
                          text="Отлично! Теперь нажмите с каким полом хотите поговорить:",
                          reply_markup=markup_find)


@bot.callback_query_handler(func=lambda user: user.data in ["find_Man", "find_Women"])
def find_candidates(message):
    user_id = message.message.chat.id
    preference = message.data.replace("find_", "")
    database.add_user(user_id, user_gender, preference)
    candidates = database.find_candidates(user_gender, preference)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Стоп", callback_data="Stop")
    markup.add(btn1)
    bot.edit_message_text(chat_id=user_id, message_id=message.message.message_id,
                          text="Ищем вам кандидата, подождите...", reply_markup=markup)

    if candidates:
        bot.edit_message_text(chat_id=user_id, message_id=message.message.message_id,
                              text="Мы вам нашли кандидата по вашим запросам\nНачните общение отправив сообщение",
                              reply_markup=markup)
        communication_user(candidates[0], markup)
    else:
        bot.edit_message_text(chat_id=user_id, message_id=message.message.message_id,
                              text="Похоже сейчас никого нет в онлайне,Подождем еще некоторое время, возможно,"
                                   " кто-то появится в онлайне и захочет пообщаться.",
                              reply_markup=markup)


def communication_user(candidate_id, markup):
    @bot.message_handler(content_types=["text"])
    def handle_message(message):
        bot.send_message(candidate_id, message.text, reply_markup=markup)


@bot.callback_query_handler(func=lambda stop: stop.data == "Stop")
def stop_talking(stop):
    user_id = stop.message.chat.id
    database.delete_user(user_id)
    bot.send_message(user_id, "Вы прекратили общение\n"
                              "Нажмите на /start чтобы вернуться в главное меню")


bot.polling()
