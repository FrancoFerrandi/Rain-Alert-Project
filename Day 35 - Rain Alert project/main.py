import requests # work with APIs
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
api_key = os.getenv("api_key")
OWM_ENDPOINT="https://api.openweathermap.org/data/2.5/forecast"

my_lat = float(-38.725151)
my_long = float(-62.254951)
my_pos = (my_long, my_lat)


weather_parameters = {
        "lat": my_lat,
        "lon": my_long,   # tener cuidado porque la nomenclatura para los parametros cambia
        "appid": api_key,
        "cnt": 4
    }

response = requests.get(url=OWM_ENDPOINT, params=weather_parameters)
print(response.status_code) #para saber si la respuesta esta bien o si tuvimos algun error de parametres
response.raise_for_status()
# print(response) # si ejecutamos directamente nos tiraria error porque hay ciertos parametros
# que en la documentacion nos dice que son obligatorios
weather_data = response.json() # primero debemos convertirla a json y guardarla en una variable
print(weather_data)

will_rain = False
for n in range(0, len(weather_data["list"])):
    condition_code = weather_data["list"][n]["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid,auth_token)
    message = client.messages \
        .create(
                body="It's going to rain in Bahia Blanca. Remember to bring an ☂️. Besos de franquito",
                from_='+12515777987',
                to='+542914614257')
    print(message.status) # verificar si se esta mandando correctamente el mensaje

