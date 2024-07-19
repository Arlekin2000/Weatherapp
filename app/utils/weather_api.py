import requests
import json


def get_weather(lat, lon):
    response = requests.get(
        f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}'
        f'&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m')
    return response.json()


if __name__ == "__main__":
    print(json.dumps(get_weather(52.52, 13.41), indent=4))
