import requests
from flask import Blueprint, render_template, g, request, url_for, redirect, make_response, get_flashed_messages
from ..app_forms import UserLoginForm, UserRegisterForm
from settings import settings

__all__ = ["index_blueprint"]

index_blueprint = Blueprint("index", "__name__")


@index_blueprint.get("/")
def index_get():
    login_form = UserLoginForm()
    register_form = UserRegisterForm()

    flash_message = get_flashed_messages(category_filter=["popup_messages"])
    if flash_message:
        title, message = flash_message[0].split("_")
        return render_template("index/index.html", **g.user,
                               login_form=login_form,
                               register_form=register_form,
                               title=title,
                               message={"key": [message]})

    return render_template("index/index.html", **g.user,
                           login_form=login_form,
                           register_form=register_form)


@index_blueprint.post("/")
def index_post():
    register_url = settings.API_GATEWAY_URL + "/registration/"
    login_url = settings.API_GATEWAY_URL + "/login/"
    form = request.form
    if len(form) == 3:
        login_form = UserLoginForm(form)
        login_form.validate()
        if login_form.errors:
            return render_template("index/index.html", **g.user,
                                   login_form=login_form,
                                   register_form=UserRegisterForm(),
                                   message=login_form.errors,
                                   title="Error")
        user_data = login_form.data
        del user_data["csrf_token"]
        response = requests.post(url=login_url, data=user_data)
    elif len(form) == 7:
        register_form = UserRegisterForm(form)
        register_form.validate()
        if register_form.errors:
            return render_template("index/index.html", **g.user,
                                   login_form=UserLoginForm(),
                                   register_form=register_form,
                                   message=register_form.errors,
                                   title="Error")
        user_data = register_form.data
        del user_data["csrf_token"]
        del user_data["repeat_password"]
        response = requests.post(url=register_url, json=user_data)

    else:
        return render_template("index/index.html", **g.user,
                               login_form=UserLoginForm(),
                               register_form=UserRegisterForm(),
                               message="Something went wrong",
                               title="Error")

    match response.status_code:
        case 200:
            jwt_token = response.json()["access_token"]
            cookie_response = make_response(redirect(url_for("index.index_get")))
            cookie_response.set_cookie('jwt_token', jwt_token, httponly=False, samesite="Lax")
            return cookie_response

        case 201:
            message = {"Reg": ["success registration"]}
            title = "Registration"

        case 403:
            message = {"Reg": ["incorrect username or password"]}
            title = "Error"

        case 409 | 422:
            message = {"Reg": ["this e-mail or username is already taken"]}
            title = "Error"

    return render_template("index/index.html", **g.user,
                           login_form=UserLoginForm(),
                           register_form=UserRegisterForm(),
                           message=message,
                           title=title)


@index_blueprint.get("/about")
def about_page():
    return render_template("index/about.html")
