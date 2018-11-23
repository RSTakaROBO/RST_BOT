# -*- coding: utf-8 -*-
import requests


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
