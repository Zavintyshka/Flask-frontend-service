import requests
from flask import Blueprint, render_template, request, redirect, url_for, make_response, g
from ..app_forms import UserDataForm
from settings import settings
from datetime import datetime

user_blueprint = Blueprint("user", __name__)


# Registration

@user_blueprint.route("/user-profile/", methods=["GET", "POST"])
def user_profile_view():
    user_data = g.user["user"]
    if not user_data:
        return redirect(url_for("user.not_authorized_view"))

    user_data["registered_at"] = datetime.strptime(user_data["registered_at"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
        "%m/%d/%Y %H:%M")
    filled_form = UserDataForm(**user_data)
    match request.method:
        case "GET":
            return render_template("user/user-profile.html", form=filled_form, user=user_data)
        case "POST":
            new_user_data_form = dict(request.form)
            url = f"{settings.API_GATEWAY_URL}/user/account/"
            jwt_token = request.cookies["jwt_token"]
            header = {"Authorization": f"Bearer {jwt_token}"}
            requests.put(url, headers=header, json=new_user_data_form)
            return redirect(url_for("user.user_profile_view"))


@user_blueprint.get("/registration/success_registration/")
def success_registration_view():
    return render_template("user/success_registration.html", message="Success Registration :)")


@user_blueprint.get("/login/error/")
def wrong_credentials_view():
    return render_template("errors/standard_error_page.html",
                           message="Incorrect password or login. Try again.")


@user_blueprint.get("/registration/error/")
def incorrect_registration_data_view():
    return render_template("errors/standard_error_page.html",
                           message="Some of your data was incorrect while registration process. Please try again.")

@user_blueprint.get("/user-profile/not-authorized/")
def not_authorized_view():
    return render_template("errors/standard_error_page.html",
                           message="You need to be authorized to view this page."), 401


@user_blueprint.get("/login/logout/")
def logout_view():
    response = make_response(redirect(location=url_for("index.index_get")))
    response.set_cookie("jwt_token", '', expires=0, httponly=True)
    return response
