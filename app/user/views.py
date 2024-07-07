import requests
from flask import Blueprint, render_template, request, redirect, url_for, make_response, g
from ..middleware import middleware
from settings import settings

user_blueprint = Blueprint("user", __name__)


# Registration

@user_blueprint.get("/registration/success_registration/")
def success_registration_view():
    return render_template("user/success_registration.html")


@user_blueprint.get("/registration/error/")
def error_view():
    return render_template("user/some_errors.html")



@user_blueprint.get("/account/")
def account_view():
    return render_template("user/account_page.html", **g.user)
