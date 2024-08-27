import requests
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, make_response, g, flash
from ..app_forms import UserDataForm
from ..app_forms import ChangePasswordForm, ResetPasswordForm
from ..middleware import make_authenticated_request
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
    achievement_list = make_authenticated_request("GET", url=url, jwt_token=jwt_token).json()

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
            make_authenticated_request("PUT", url=url, jwt_token=jwt_token, json=user_data_json)
            return redirect(url_for("user.user_profile_view"))


@user_blueprint.get("/<string:username>/my-files/")
def user_files_view(username: str):
    user_data = g.user["user"]

    if not user_data or not user_data["username"] == username:
        return redirect(url_for("user.not_authorized_view"))

    url = f"{settings.API_GATEWAY_URL}/video/pairs_list"
    jwt_token = request.cookies["jwt_token"]
    action_list = make_authenticated_request("GET", url=url, jwt_token=jwt_token).json()
    for row in action_list:
        row["converted_filename"] = Path(row["raw_filename"]).stem + "_converted." + row["converted_file_extension"]

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
    response.set_cookie("jwt_token", '', expires=0, httponly=False)
    return response


@user_blueprint.get("/reset-password/")
def reset_password():
    form = ResetPasswordForm()
    return render_template("user/reset_password.html", **g.user, form=form, title="Reset Password",
                           message={"key": ["Some test text"]})


@user_blueprint.route("/change-password/<string:reset_token>", methods=["GET", "POST"])
def change_password(reset_token: str):
    api_response = requests.get(f"{settings.API_GATEWAY_URL}/user/check-token/{reset_token}")
    user_data = dict(api_response.json()) if api_response.ok else None
    match request.method:
        case "GET":
            form = ChangePasswordForm()
        case "POST":
            form = ChangePasswordForm(request.form)
            is_form_valid = form.validate()
            if not is_form_valid:
                return render_template("user/change_password.html", user_data=user_data, form=form)
            api_url = f"{settings.API_GATEWAY_URL}/user/reset-password/{reset_token}/"
            password_data = {"password": form.password.data, "repeated_password": form.repeated_password.data}
            api_response = requests.post(api_url, json=password_data)
            flash("Change Password_Password changed successfully", "popup_messages")
            return redirect(url_for("index.index_get"))

    return render_template("user/change_password.html", user_data=user_data, form=form)


def beautify_date(iso8086: str) -> str:
    return datetime.strptime(iso8086, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%m/%d/%Y %H:%M")
