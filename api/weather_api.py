import requests
from data.config import WEATHER_KEY


def transfer_of_seconds_to_hours_and_minutes(sec: int):
    hour = (sec % (24 * 3600)) // 3600
    minuts = (sec % (24 * 3600)) // 60 % 60
    return "%02d:%02d" % (hour + 3, minuts)


def give_current_weather(city: str) -> str:
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric&lang=ru"
        ).json()
        return str(
            f"Страна: {response['sys']['country']}\n"
            f"Город: {response['name']}\n"
            f"Состояние: {response['weather'][0]['description']}\n"
            f"Текущая температура: {response['main']['temp']} °C\n"
            f"Ощущается как: {response['main']['feels_like']} °C\n"
            f"Максимальная температура: {response['main']['temp_max']} °C\n"
            f"Минимальная температура: {response['main']['temp_min']} °C\n"
            f"Влажность: {response['main']['humidity']} г/м³\n"
            f"Давление: {response['main']['pressure']} Па\n"
            f"Скорость ветра: {round(response['wind']['speed'] * 3.6, 2)} км/ч\n"
            f"Восход: {transfer_of_seconds_to_hours_and_minutes(int(response['sys']['sunrise']))}, "
            f"Закат: {transfer_of_seconds_to_hours_and_minutes(int(response['sys']['sunset']))}"
        )
    except KeyError:
        return "The city is not found"
