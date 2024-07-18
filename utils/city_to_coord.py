import requests
import json

API_KEY = "Ks7cX2PgHURzr1EFWi1b1g==u7yCh1FnP8qFDEIG"


def get_coordinates(city):
    response = requests.get(
        f'https://api.api-ninjas.com/v1/geocoding?city={city}&limit=1',
        headers={'X-Api-Key': API_KEY})
    result = response.json()
    if not result or "error" in result:
        return 0, 0
    return result[0]["latitude"], result[0]["longitude"]


if __name__ == "__main__":
    print(json.dumps(get_coordinates(""), indent=4))