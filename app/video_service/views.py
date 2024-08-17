from uuid import uuid4
from flask import Blueprint, render_template, g, request, redirect, url_for, make_response
from ..middleware import make_authenticated_request
from ..redis_client import redis_connection
from settings import settings, TTL

__all__ = ["video_blueprint"]

video_blueprint = Blueprint("video", __name__)


@video_blueprint.get("/video/")
def video_editor_get():
    user_data = g.user["user"]

    if not user_data:
        return redirect(url_for("user.not_authorized_view"))

    user_session_id = request.cookies.get("user_session_id")
    if not user_session_id:
        session_id = str(uuid4())
        response = make_response(render_template("service_pages/video_page.html", **g.user))
        response.set_cookie("user_session_id", session_id, max_age=TTL)
        return response
    else:
        file_redis_data = redis_connection.get_record(user_session_id)
        redis_connection.update_expire_time(user_session_id, ttl=TTL)
        if not file_redis_data:
            file_data = None
        else:
            file_data = {"file_uuid": file_redis_data["file_uuid"], "filename": file_redis_data["filename"]}
        return render_template("service_pages/video_page.html", **g.user, file_data=file_data)


@video_blueprint.get("/video/")
def video_editor_post():
    jwt_token = request.cookies["jwt_token"]
    file = request.files["file"]
    fields = dict(request.form)
    data = {
        "filename": fields["filename"]
    }

    files = {'file': (file.filename, file.stream, file.content_type)}
    file_uuid = make_authenticated_request("POST",
                                           url=settings.API_GATEWAY_URL + "/video/file",
                                           data=data, files=files, jwt_token=jwt_token).json()["file_uuid"]

    json_data = {"file_uuid": file_uuid, "action_type": fields["action_type"], "action": fields["action"]}

    response = make_authenticated_request("POST",
                                          url=settings.API_GATEWAY_URL + "/video/processes_file",
                                          json=json_data, jwt_token=jwt_token)
    return "201"
