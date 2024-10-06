import requests
import os
from dotenv import load_dotenv
from models import SessionLocal, Weather, init_db

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'pt_br'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def store_weather(data):
    session = SessionLocal()
    weather = Weather(
        city=data.get('name'),
        temperature=data['main']['temp'],
        description=data['weather'][0]['description'],
        humidity=data['main']['humidity'],
        wind_speed=data['wind']['speed']
    )
    session.add(weather)
    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()
    cidade = input("Digite o nome da cidade: ")
    dados = get_weather(cidade)
    store_weather(dados)
    print(f"Dados de {cidade} armazenados com sucesso.")
