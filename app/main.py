from flask import Flask, request, render_template, redirect, make_response
from app.utils.weather_api import get_weather
from app.utils.city_to_coord import get_coordinates
from app.models import User, UserHistory, City
from app.utils.auth import check_auth
import peewee as pw


app = Flask(__name__)


@app.route("/register", methods=["POST", "GET"])
async def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        data = request.form.to_dict()
        user = User.select().where(User.email == data["email"]).first()
        if not user:
            User.create(email=data["email"], password=User.set_password(data["password"]))

        return redirect("/login", code=302)


@app.route("/login", methods=["POST", "GET"])
async def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        data = request.form.to_dict()
        user = User.select().where(User.email == data["email"]).first()
        if not user:
            return "User not found", 404

        if user.check_password(data["password"]):
            res = make_response(render_template("main_page.html"))
            res.set_cookie("auth", user.token)
            return res

@app.route("/")
@check_auth
async def hello(*args, **kwargs):
    return render_template("main_page.html")


@app.route("/get_weather", methods=["POST"])
@check_auth
async def get_weather_data(user: User):
    city = request.form.get("city")
    city = get_coordinates(city)
    if not city:
        return "City not found", 404

    UserHistory.insert(city=city, user=user).execute()

    data = get_weather(city.latitude, city.longitude)
    date, time = data['current']['time'].split("T")
    return render_template(
        "main_page.html",
        time=time,
        date=date,
        temperature=data['current']['temperature_2m'],
        wind=data['current']['wind_speed_10m'],
        hourly=data["hourly"],
        city=city.name,
        user=user
        )


@app.route("/city_statistics", methods=["GET"])
async def get_city_statistics():
    stats = (
        UserHistory.select(
            City.id,
            City.name,
            pw.fn.COUNT(City.id).alias("count"),
        )
        .join(City, on=(City.id == UserHistory.city_id))
        .group_by(UserHistory.city_id)
    )

    return list(stats.dicts())


if __name__ == "__main__":
    app.run(debug=True)

#посмотреть автодополнение во фласк