import os
import peewee as pw
from hashlib import md5
import jwt
import datetime as dt

JWT_SECRET = "$ECRET~!23"
if os.environ.get("ENV") == "tests":
    db = pw.SqliteDatabase("test.sqlite")
    db.connect()
else:
    db = pw.SqliteDatabase("db1.sqlite")
    db.connect()


class User(pw.Model):
    id: int
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=True)
    class Meta:
        database = db

    @property
    def token(self):
        return jwt.encode(
            {
                "id": self.id,
                "login": self.email,
                "exp": (dt.datetime.utcnow() + dt.timedelta(days=30)).timestamp()
            },
            key=JWT_SECRET,
            )

    @classmethod
    def set_password(cls, password):
        return md5(password.encode("utf-8")).hexdigest()

    def check_password(self, password):
        return self.password == md5(password.encode('utf-8')).hexdigest()

    @classmethod
    def load_from_token(cls, token):
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            unow = dt.datetime.utcnow()
            exp = dt.datetime.fromtimestamp(data["exp"])
            if unow > exp:
                return None

            return cls.select().where(cls.id == data["id"]).first()
        except (jwt.InvalidTokenError, KeyError):
            return None


class City(pw.Model):
    id: int
    name = pw.CharField()
    latitude = pw.CharField()
    longitude = pw.CharField()
    class Meta:
        database = db

class UserHistory(pw.Model):
    id: int
    city = pw.ForeignKeyField(column_name="city_id", model=City)
    user = pw.ForeignKeyField(column_name="user_id", model=User)
    class Meta:
        database = db

    @classmethod
    def get_last_city_for_user(cls, user_id):
        return cls.select().where(cls.user == user_id).order_by(cls.id.desc()).first()
    