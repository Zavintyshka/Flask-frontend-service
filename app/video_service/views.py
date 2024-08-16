from flask import Blueprint, render_template, g, request, redirect, url_for
from ..middleware import make_authenticated_request
from settings import settings

__all__ = ["video_blueprint"]

video_blueprint = Blueprint("video", __name__)


@video_blueprint.route("/video", methods=["GET", "POST"])
def video_editor():
    user_data = g.user["user"]

    if not user_data:
        return redirect(url_for("user.not_authorized_view"))

    jwt_token = request.cookies["jwt_token"]
    match request.method:
        case "GET":
            return render_template("service_pages/video_page.html", **g.user)
        case "POST":
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
