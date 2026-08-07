import json
import requests
from kafka import KafkaProducer

# Kafka configuration
TOPIC = "kenya_weather"
producer = KafkaProducer(bootstrap_servers="kafka:9092",value_serializer=lambda v: json.dumps(v).encode("utf-8"),api_version=(2, 8, 1),)

CITIES = {
    "Nairobi": (-1.286389, 36.817223),
    "Mombasa": (-4.043477, 39.668206),
    "Kisumu": (-0.091702, 34.767956),
    "Nakuru": (-0.303099, 36.080025),
    "Eldoret": (0.514277, 35.269779),
    "Thika": (-1.033260, 37.069330),
    "Malindi": (-3.219186, 40.116890),
    "Garissa": (-0.453229, 39.646011),
    "Kitale": (1.015720, 35.006220),
    "Nyeri": (-0.420130, 36.947590),
}

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_forecast(city, lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "relative_humidity_2m_mean",
            "wind_speed_10m_max"
        ],
        "forecast_days": 2,
        "timezone": "Africa/Nairobi"
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    forecast_date = data["daily"]["time"][1]

    return {
        forecast_date: {
            "city": city,
            "temperature": data["daily"]["temperature_2m_max"][1],
            "humidity": data["daily"]["relative_humidity_2m_mean"][1],
            "wind_speed": data["daily"]["wind_speed_10m_max"][1]
        }
    }


def main():
    for city, (lat, lon) in CITIES.items():
        weather = get_forecast(city, lat, lon)

        producer.send(TOPIC, weather)
        print(f"Produced: {weather}")

    producer.flush()
    producer.close()

if __name__ == "__main__":
    main()