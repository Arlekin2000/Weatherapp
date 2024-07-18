from flask import Flask, request
from flask import render_template
from utils.weather_api import get_weather
from utils.city_to_coord import get_coordinates
import peewee as pw


app = Flask(__name__)
db = pw.SqliteDatabase("db.sqlite")


@app.route("/")
async def hello():
    return render_template("main_page.html")


@app.route("/get_weather", methods=["POST"])
async def get_weather_data():
    #{'latitude': 52.52, 'longitude': 13.419998, 'generationtime_ms': 0.053048133850097656, 'utc_offset_seconds': 0, 'timezone': 'GMT', 'timezone_abbreviation': 'GMT', 'elevation': 38.0, 'current_units': {'time': 'iso8601', 'interval': 'seconds', 'temperature_2m': '°C', 'wind_speed_10m': 'km/h'}, 'current': {'time': '2024-07-17T17:15', 'interval': 900, 'temperature_2m': 22.3, 'wind_speed_10m': 11.7}}
    city = request.form.get("city")
    coords = get_coordinates(city)
    latitude, longitude = coords
    data = get_weather(latitude, longitude)
    date, time = data['current']['time'].split("T")
    return render_template(
        "main_page.html",
        time=time,
        date=date,
        temperature=data['current']['temperature_2m'],
        wind=data['current']['wind_speed_10m'],
        hourly=data["hourly"],
        city=city)


if __name__ == "__main__":
    app.run(debug=True)

#посмотреть автодополнение во фласк