import requests
from flask import Blueprint, render_template, request, redirect, url_for, make_response, g
from ..app_forms import UserDataForm
from settings import settings
from datetime import datetime

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/user-profile/", methods=["GET", "POST"])
def user_profile_view():
    user_data = g.user["user"]

    if not user_data:
        return redirect(url_for("user.not_authorized_view"))

    user_data["registered_at"] = beautify_date(user_data["registered_at"])
    filled_form = UserDataForm(**user_data)

    url = f"{settings.API_GATEWAY_URL}/user/achievement/"
    jwt_token = request.cookies["jwt_token"]
    header = {"Authorization": f"Bearer {jwt_token}"}
    achievement_list = requests.get(url, headers=header).json()

    achievement_list_video = []
    achievement_list_image = []
    achievement_list_audio = []

    for achievement in achievement_list:
        service_type = achievement["service"]
        match service_type:
            case "video":
                achievement_list_video.append(achievement)
            case "image":
                achievement_list_image.append(achievement)
            case "audio":
                achievement_list_audio.append(achievement)

    match request.method:
        case "GET":
            return render_template("user/user_profile.html",
                                   form=filled_form,
                                   user=user_data,
                                   achievement_list_video=achievement_list_video,
                                   achievement_list_image=achievement_list_image,
                                   achievement_list_audio=achievement_list_audio)
        case "POST":
            user_data_form = UserDataForm(request.form)

            if not user_data_form.validate():
                return render_template("user/user_profile.html", form=user_data_form, user=user_data)

            user_data_json = user_data_form.data
            del user_data_json["registered_at"]
            del user_data_json["username"]
            url = f"{settings.API_GATEWAY_URL}/user/account/"
            jwt_token = request.cookies["jwt_token"]
            header = {"Authorization": f"Bearer {jwt_token}"}
            requests.put(url, headers=header, json=user_data_json)
            return redirect(url_for("user.user_profile_view"))


@user_blueprint.get("/<string:username>/my-files/")
def user_files_view(username: str):
    user_data = g.user["user"]

    if not user_data or not user_data["username"] == username:
        return redirect(url_for("user.not_authorized_view"))

    url = f"{settings.API_GATEWAY_URL}/video/pairs_list"
    jwt_token = request.cookies["jwt_token"]
    header = {"Authorization": f"Bearer {jwt_token}"}
    action_list = requests.get(url, headers=header).json()
    return render_template("user/user_files.html", action_list=action_list, user=user_data)


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


def beautify_date(iso8086: str) -> str:
    return datetime.strptime(iso8086, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%m/%d/%Y %H:%M")
