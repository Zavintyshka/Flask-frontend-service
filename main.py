import requests
from typing import Optional
from flask import Flask, render_template, request, redirect, url_for, make_response, g
from settings import settings

server = Flask(__name__)


@server.before_request
def get_current_user():
    user_jwt_token: Optional[str] = request.cookies.get("jwt_token")
    if not user_jwt_token:
        g.user = {"user": None}
    url = settings.API_GATEWAY_URL + "user/account/"
    header = {"Authorization": f"Bearer {user_jwt_token}"}
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        user_data: dict = response.json()
        g.user = {"user": user_data}
    else:
        g.user = {"user": None}


@server.get("/")
def index():
    return render_template("index.html", **g.user)


# Registration

@server.get("/registration/success_registration/")
def success_registration_view():
    return render_template("success_registration.html")


@server.get("/registration/error/")
def error_view():
    return render_template("some_errors.html")


@server.route("/registration/", methods=["GET", "POST"])
def registration_view():
    method = request.method
    match method:
        case "GET":
            return render_template("registration.html")
        case "POST":
            fields = ("username", "firstname", "lastname", "email", "password")
            user = {field: request.form.get(field) for field in fields}
            url = settings.API_GATEWAY_URL + "registration/"
            response = requests.post(url=url, json=user)
            match response.status_code:
                case 201:
                    return redirect(location=url_for("success_registration_view"))
                case _:
                    return redirect(location=url_for("error_view"))


# Login / Logout

@server.route("/login/", methods=["GET", "POST"])
def login_view():
    method = request.method
    match method:
        case "GET":
            return render_template("login_page.html")
        case "POST":
            fields = ("username", "password")
            user = {field: request.form.get(field) for field in fields}
            url = settings.API_GATEWAY_URL + "login/"
            token_data = requests.post(url=url, data=user).json()
            jwt_token = token_data["access_token"]
            print(jwt_token)
            response = make_response(redirect(url_for("index")))
            response.set_cookie('jwt_token', jwt_token, httponly=True)
            return response


@server.get("/login/logout/")
def logout_view():
    response = make_response(redirect(location=url_for("index")))
    response.set_cookie("jwt_token", '', expires=0, httponly=True)
    return response


# Account

@server.get("/account/")
def account_view():
    return render_template("account_page.html", **g.user)
