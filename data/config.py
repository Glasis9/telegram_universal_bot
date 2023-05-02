import os

from dotenv import load_dotenv

load_dotenv()


WEATHER_KEY = os.getenv("WEATHER_KEY")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
