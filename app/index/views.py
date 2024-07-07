import requests
from flask import Blueprint, render_template, g, request, url_for, redirect, make_response
from settings import settings

__all__ = ["index_blueprint"]

index_blueprint = Blueprint("index", "__name__")


@index_blueprint.get("/")
def index_get():
    return render_template("index/index.html", **g.user)


@index_blueprint.post("/")
def index_post():
    register_url = settings.API_GATEWAY_URL + "/registration/"
    login_url = settings.API_GATEWAY_URL + "/login/"
    form = request.form
    if len(form) < 4:
        user_data = {field: form.get(field) for field in ("username", "password")}
        response = requests.post(url=login_url, data=user_data)
    else:
        user_data = {field: form.get(field) for field in ("username", "firstname", "lastname", "email", "password")}
        response = requests.post(url=register_url, json=user_data)

    match response.status_code:
        case 201:
            print("Создана учетная запись")
            return redirect(url_for("user.success_registration_view"))
        case 200:
            jwt_token = response.json()["access_token"]
            cookie_response = make_response(redirect(url_for("index.index_get")))
            cookie_response.set_cookie('jwt_token', jwt_token, httponly=True)
            return cookie_response
        case _:
            return redirect(url_for("user.error_view"))
