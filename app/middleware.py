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
        url = settings.API_GATEWAY_URL + "/user/account/"
        header = {"Authorization": f"Bearer {user_jwt_token}"}
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            user_data: dict = response.json()
            g.user = {"user": user_data}
            print("Доступ есть")
        else:
            g.user = {"user": None}
            print("Доступа нет")

