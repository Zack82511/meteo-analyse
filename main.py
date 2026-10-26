import requests as rq
import sqlite3 as sql
import matplotlib.pyplot as plt

conn = sql.connect("data/meteo_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS meteo_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    wind_speed REAL,
    day_night TEXT,
    timestamp TEXT,
    rain REAL,
    snowfall REAL,
    cloud_cover REAL
)""")
conn.commit()

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": "46.35",
    "longitude": "-72.55",
    "current": "temperature_2m,wind_speed_10m,is_day,rain,snowfall,cloud_cover",
    "timezone": "auto"
}
params_hourly = {
    "latitude": "46.35",
    "longitude": "-72.55",
    "hourly": "temperature_2m,wind_speed_10m,rain,snowfall,cloud_cover",
    "timezone": "auto"
}
green = "\033[92m"
reset = "\033[0m"
def meteo():
    try:
        response = rq.get(url, params=params, timeout=5) 
        response.raise_for_status()
        data = response.json()["current"] # Extract the current weather data
        temperature = data["temperature_2m"] 
        wind_speed = data["wind_speed_10m"]
        is_day = data["is_day"]
        if is_day == 1:
            day_night = "day"
        elif is_day == 0:
            day_night = "night"
        else:
            day_night = "unknown"
        timestamp = data["time"]
        rain = data["rain"]
        snowfall = data["snowfall"]
        cloud_cover = data["cloud_cover"]
        
                
        return {
            "temperature": temperature,
            "wind_speed": wind_speed,
            "day_night": day_night,
            "timestamp": timestamp,
            "rain": rain,
            "snowfall": snowfall,
            "cloud_cover": cloud_cover
        }
        
        
        
    except rq.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except KeyError as e:
        print(f"Missing expected data in the response: {e}")
    except sql.Error as e:
        print(f"Database error: {e}")
try:
    weather_data = meteo()
    if weather_data:
        print("Current Weather Data:")
        print(f"Temperature: {green}{weather_data['temperature']}°C{reset}")
        print(f"Wind Speed: {green}{weather_data['wind_speed']} km/h{reset}")
        print(f"Day/Night: {green}{weather_data['day_night']}{reset}")
        print(f"Timestamp: {green}{weather_data['timestamp']}{reset}")
        print(f"Rain: {green}{weather_data['rain']} mm{reset}")
        print(f"Snowfall: {green}{weather_data['snowfall']} mm{reset}")
        print(f"Cloud Cover: {green}{weather_data['cloud_cover']}%{reset}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

    

def hourly_plot():
    try:
        response = rq.get(url, params=params_hourly, timeout=5)
        response.raise_for_status
        data = response.json()["hourly"]
        timestamp = data["time"]
        rain = data["rain"]
        snowfall = data["snowfall"]
        cloud_cover = data["cloud_cover"]
        temperature = data["temperature_2m"] 
        wind_speed = data["wind_speed_10m"]
        plt.plot(timestamp, wind_speed)
        plt.xticks(range(0,len(timestamp), 24), [t[5:10] for t in timestamp[::24]], rotation=45)
        plt.show()
    except rq.exceptions.RequestException as e:
        print(f"rquest error {e}")
    except KeyError as e:
        print(f"key error {e}")

hourly_plot()