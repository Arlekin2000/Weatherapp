import requests
import json
from app.models import City

API_KEY = "Ks7cX2PgHURzr1EFWi1b1g==u7yCh1FnP8qFDEIG"


def get_coordinates(city_name):
    city = City.select().where(City.name == city_name).first()
    if not city:
        response = requests.get(
            f'https://api.api-ninjas.com/v1/geocoding?city={city_name}&limit=1',
            headers={'X-Api-Key': API_KEY})
        result = response.json()
        if not result or "error" in result:
            return None
        city = City.create(
            name=city_name,
            latitude=result[0]["latitude"],
            longitude=result[0]["longitude"]
        )
    return city


if __name__ == "__main__":
    print(json.dumps(get_coordinates(""), indent=4))