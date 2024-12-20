import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

def load_env_variables() -> None:
    """Cargar las variables de entorno desde el archivo .env."""
    load_dotenv()


def validate_env_variables(*variables: str) -> None:
    """Validar que todas las variables requeridas estén definidas."""
    missing = [var for var in variables if not os.getenv(var)]
    if missing:
        print(f"Faltan las siguientes variables de entorno: {', '.join(missing)}")
        exit(1)


def fetch_weather(lat: float, lon: float, api_key: str) -> dict:
    """Obtener los datos del clima desde la API de OpenWeather."""
    endpoint = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "cnt": 4  #4 intervalos = 12 hs (tiempo que verifica si va a llover o no)
    }
    try:
        response = requests.get(url=endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos del clima: {e}")
        exit(1)


def will_it_rain(weather_data: dict) -> bool:
    """Determinar si lloverá basándose en los datos del clima."""
    for forecast in weather_data.get("list", []):
        condition_code = forecast["weather"][0]["id"]
        if int(condition_code) < 700:
            return True, forecast["dt_txt"]
    return False, None


def send_alert(account_sid: str, auth_token: str, to: str, from_: str, message_body: str) -> None:
    """Enviar un mensaje de alerta usando Twilio."""
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(body=message_body, from_=from_, to=to)
        print(f"Mensaje enviado correctamente. Estado: {message.status}")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
        exit(1)
