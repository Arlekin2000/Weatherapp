from flask import request, redirect

from app.models import User


def check_auth(func):
    async def wrapper(*args, **kwargs):
        token = request.cookies.get("auth")
        if not token:
            return redirect("/login")

        user = User.load_from_token(token)
        if not user:
            return "User not found", 404

        return await func(user, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
