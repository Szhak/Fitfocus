import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = '33fac9b8a1f34383baa96a4b0ab90198'
CLIENT_SECRET = '55ae82a8bcb64578bf03ba7d8433a82e'

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))


def send_music(message):
    try:
        results = sp.search(q=message, limit=1, type='track')
        if results['tracks']['items']:
            track_url = results['tracks']['items'][0]['external_urls']['spotify']
            a = f""" Вот ссылка на эту музыку '{message}': {track_url}
Вставьте ссылку которую вам дал бот сюда https://spotifydown.com/ru 
Скоро бот научится скачивать...
(Да-да подразумеваю себя)
            """
        else:
            a = "Музыка не найдена"

    except Exception as e:
        a = f"Произошла непредвиденная ошибка: {e}\n Попробуйте позднее"
    return a


def calories(height, weight, age, gen, activ, want):
    want_dict = {"defecate": 90, "saving": 100, "surplus": 110}
    active_dict = {"few": 0.8, "normal": 1, "high": 1.2}
    if gen == "boy":
        a = ((10 * height) + (6.25 + weight) - (5 * age) + 5) * active_dict[activ]

        return (a * want_dict[want]) / 100
    elif gen == "girl":
        a = ((10 * height) + (6.25 + weight) - (5 * age) - 161) * active_dict[activ]

        return (a * want_dict[want]) / 100


def protein_and_fat(callories):
    return (callories * 30) / 100


def carbohydrate(callories):
    return (callories * 40) / 100


def left_cpfc(cpfc_need, cpfc):  # Выводит сколько осталось употребить кБЖУ
    lft = []
    for i in range(4):
        a = cpfc_need[i] - cpfc[i]
        if a > 0:
            lft.append(int(a))
        else:
            lft.append(f"{int(a)}  Вот на столько вы превысили")
    return lft


def product(name):
    list_numbers = []
    list_name = []
    num = ""
    for word in name:
        if word.replace('.', '').isdigit():
            num += word
        else:
            if num:
                list_numbers.append(float(num))
                num = ""
            list_name.append(word)
        if num:
            list_numbers.append(float(num))
    return [''.join(list_name)], list_numbers


