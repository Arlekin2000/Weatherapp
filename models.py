import peewee as pw
from main import db


class User(pw.Model):
    id: int
    login = pw.CharField(unique=True)
    password = pw.CharField(unique=True)


class City(pw.Model):
    id: int
    name = pw.CharField()
    latitude = pw.CharField()
    longitude = pw.CharField()


class UserHistory(pw.Model):
    id: int
    city = pw.ForeignKeyField(column_name="city_id", model=City)
    user = pw.ForeignKeyField(column_name="user_id", model=User)
