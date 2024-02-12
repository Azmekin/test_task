import os

import requests
from dotenv import load_dotenv
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_TOKEN")

def call_weather(city:str):
    r=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}")
    return r