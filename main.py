import requests as rq

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": "46.35",
    "longitude": "-72.55",
    "current": "temperature_2m,wind_speed_10m",
    "timezone": "auto"
}
try:
    response = rq.get(url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()["current"]
    temperature = data["temperature_2m"]
    wind_speed = data["wind_speed_10m"]
    timestamp = data["time"]
    print(f"Il fait acuellement {temperature}°C avec une vitesse du vent de {wind_speed} km/h à {timestamp}.")

except rq.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except KeyError as e:
    print(f"Missing expected data in the response: {e}")