# -*- coding: utf-8 -*-
import requests
import json
import datetime
import time
import random
import weather_bot

BOT_TOKEN = '61236655:AAGCHX7Pmyd4gdU1XQvaG5iZaf371cnrigo'
SPLIT_WORD = 'или'.decode("utf-8")
TELEGRAM_URL = 'https://api.telegram.org/bot'


class dialog():

    def __init__(self, user_id, dlg_id, username):
        self.username = username
        self.user_id = user_id
        self.status = 0
        self.id = dlg_id
        print('new dialog created')

    def run(self, message, user_id):
        if self.id == 1:
            self.give_advice(message, user_id)

    def give_advice(self, message, user_id):
        if self.status == 0:
            send_message(self.user_id, '{}, давай попробую!'.format(self.username).decode("utf-8"))
            self.status += 1
            return

        if self.user_id == user_id:
            user_message = message
            user_words = user_message.split(' ')
            print user_words
            if SPLIT_WORD in user_words:
                or_position = user_message.split(SPLIT_WORD)
                r = random.randint(0, len(or_position)-1)
                send_message(self.user_id, or_position[r])
            else:
                send_message(self.user_id, 'Ну тут всё очевидно, согласись'.decode("utf-8"))
            self.status = -1


def get_frist_update():
    r = requests.get(TELEGRAM_URL + BOT_TOKEN + '/getUpdates', auth=('user', 'pass'))
    data = r.json()
    if len(data["result"]) == 0:
        return 0
    return data["result"][0]["update_id"]


def get_upate(offset):
    r = requests.get(TELEGRAM_URL + BOT_TOKEN + '/getUpdates?timeout=20&offset=' + str(offset),
                     auth=('user', 'pass'))
    data = r.json()
    return data


def send_message(user_id, message):
    send_message_url = TELEGRAM_URL + BOT_TOKEN + '/sendMessage?chat_id=' + str(
        user_id) + '&text=' + message
    requests.post(send_message_url, auth=('user', 'pass'))


offset = get_frist_update()
dialogs = []

while True:

    update = get_upate(offset + 1)
    if len(update["result"]) == 0:
        print("nothing")
        time.sleep(1)
        continue

    print(update["result"])

    for x in range(0, len(update["result"])):

        if "message" in update["result"][x]:
            print('message')
            user_id = update["result"][x]["message"]["from"]["id"]
            username = update["result"][x]["message"]["from"]["username"]
            user_message = update["result"][x]["message"]["text"].lower()
        else:
            print('inline_query')
            print update["result"][x]["inline_query"]["query"]
            user_id = update["result"][x]["inline_query"]["from"]["id"]
            username = update["result"][x]["inline_query"]["from"]["username"]
            user_message = update["result"][x]["inline_query"]["query"].lower()

        if user_message == 'посоветуй'.decode("utf-8"):
            dialogs.append(dialog(user_id, 1, username))

        if user_message == 'погода'.decode("utf-8"):
            send_message(user_id, weather_bot.get_weather("now"))

        if user_message == 'прогноз'.decode("utf-8"):
            send_message(user_id, weather_bot.get_weather("day"))

        if user_message == 'спасибо'.decode("utf-8"):
            send_message(user_id, "Пожалуйста! :)")

        print('checking dialogs')
        for x in range(0, len(dialogs)):
            if dialogs[x].status == -1:
                continue
            print('run dialog')
            dialogs[x].run(user_message, user_id)

    offset = update["result"][len(update["result"]) - 1]["update_id"]
    time.sleep(1)
