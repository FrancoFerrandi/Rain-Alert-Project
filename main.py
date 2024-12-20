import os
import json
from weather_alert_utils import load_env_variables, validate_env_variables, fetch_weather, will_it_rain, send_alert


load_env_variables()

# Validar variables de entorno
required_vars = ["account_sid", "auth_token", "api_key", "twilio_number", "recipient_number"]
validate_env_variables(*required_vars)
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
api_key = os.getenv("api_key")
twilio_number = os.getenv("twilio_number")
recipient_number = os.getenv("recipient_number")

# Ubicación de Buenos Aires
my_lat = -34.603683
my_long = -58.381557

# Obtener datos del clima
weather_data = fetch_weather(lat=my_lat, lon=my_long, api_key=api_key)
print("Datos del clima:")
print(json.dumps(weather_data, indent=4))

# Verificar si lloverá
rain, time = will_it_rain(weather_data)
if rain:
    message_body = (
        f"Va a llover en Buenos Aires el {time}. ☔️ Lleva un paraguas. Besos de Franquito."
    )
    send_alert(
        account_sid=account_sid,
        auth_token=auth_token,
        to=recipient_number,
        from_=twilio_number,
        message_body=message_body
    )
else:
    print("No se espera lluvia en las próximas horas.")

