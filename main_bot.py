# -*- coding: utf-8 -*-
import requests
import json
import datetime
import time

BOT_TOKEN = '61236655:AAGCHX7Pmyd4gdU1XQvaG5iZaf371cnrigo'


def get_weather(forecast_type):

    curr_weather_text = 'В  {}  сейчас: {} температура:  {}'.decode("utf-8")
    day_weather_text = "В {} сегодня {}:\n🌅 Утром: {}°\n🌇 Днем :{}°\n🌄 Вечером: {}°\n🌃 Ночью:{}°".decode("utf-8")

    if forecast_type != "now" and forecast_type != "day":
        return "nothing"

    r = requests.get('http://pogoda.onliner.by/sdapi/pogoda/api/forecast/26850')
    weather_data = r.json()
    city = weather_data["city"]

    if forecast_type == "now":
        status = weather_data["now"]["phenomena"]
        curr_temp = weather_data["now"]["temperature"]
        return_string = curr_weather_text.format(city, status, curr_temp)

    if forecast_type == "day":
        curr_day = weather_data["today"]["date"]
        morning = weather_data["today"]["morning"]["temperature"]
        day = weather_data["today"]["day"]["temperature"]
        evening = weather_data["today"]["evening"]["temperature"]
        night = weather_data["today"]["night"]["temperature"]
        return_string = day_weather_text.format(city, curr_day, morning, day, evening, night)

    return return_string


def get_frist_update():
    r = requests.get('https://api.telegram.org/bot' + BOT_TOKEN + '/getUpdates', auth=('user', 'pass'))
    data = r.json()
    if len(data["result"]) == 0:
        return 0
    return data["result"][0]["update_id"]


def get_upate(offset):
    r = requests.get('https://api.telegram.org/bot' + BOT_TOKEN + '/getUpdates?timeout=20&offset=' + str(offset),
                     auth=('user', 'pass'))
    data = r.json()
    return data


def send_message(user_id, message):
    send_message_url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + str(
        user_id) + '&text=' + message
    requests.post(send_message_url, auth=('user', 'pass'))


offset = get_frist_update()

while True:

    update = get_upate(offset + 1)
    if len(update["result"]) == 0:
        print("nothing")
        time.sleep(1)
        continue
    print(update)

    for x in range(0, len(update["result"])):

        user_id = update["result"][x]["message"]["from"]["id"]
        user_message = update["result"][x]["message"]["text"].lower()
        message_to_send = ""

        if user_message == '/weather':
            print ("sending message to", user_id)
            send_message(user_id, get_weather("now"))
        if user_message == '/weatherday':
            print ("sending message to", user_id)
            send_message(user_id, get_weather("day"))
        if user_message == 'спасибо':
            print ("sending message to", user_id)
            send_message(user_id, "Пожалуйста! :)")

    offset = update["result"][len(update["result"]) - 1]["update_id"]
    time.sleep(1)
