import requests
from typing import Optional
from flask import request, g
from settings import settings


def middleware(app):
    @app.before_request
    def get_current_user():
        user_jwt_token: Optional[str] = request.cookies.get("jwt_token")
        if not user_jwt_token:
            g.user = {"user": None}
            return
        if "static" in request.url:
            return
        url = settings.API_GATEWAY_URL + "/user/account/"
        response = make_authenticated_request("GET", url, jwt_token=user_jwt_token)
        if response.status_code == 200:
            user_data: dict = response.json()
            g.user = {"user": user_data}
        else:
            g.user = {"user": None}


def make_authenticated_request(method: str, url: str, jwt_token: str, **kwargs) -> requests.Response:
    match method.upper():
        case "GET":
            request_func = requests.get
        case "POST":
            request_func = requests.post
        case "PUT":
            request_func = requests.put
        case _:
            raise Exception("Invalid request method")
    headers = {"Authorization": f"Bearer {jwt_token}"}
    return request_func(url=url, headers=headers, **kwargs)
