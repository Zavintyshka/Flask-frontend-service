from uuid import uuid4
import shutil
from pathlib import Path
from flask import Blueprint, request, Response, send_from_directory
from settings import PRELOAD_FOLDER, TTL
from .redis_client import redis_connection

preloader_blueprint = Blueprint("preloader", __name__)


@preloader_blueprint.post("/preload/")
def preload_user_file():
    user_session_id = request.cookies.get("user_session_id")
    if not user_session_id:
        return Response(status=403)

    file = request.files.get("file")
    filename = Path(request.form.get("filename"))
    file_ext = filename.suffix
    filename_uuid = f"{uuid4()}{file_ext}"
    file_path = Path(PRELOAD_FOLDER) / user_session_id / filename_uuid
    if file_path.parent.exists():
        shutil.rmtree(file_path.parent)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("wb") as file_obj:
        file.save(file_obj)
    data = {"filename": str(filename), "file_uuid": filename_uuid, "service": "video"}
    redis_connection.make_record(user_session_id, data=data, ttl=TTL)
    return Response(status=201)


@preloader_blueprint.get("/preload/<string:file_uuid>/")
def load_user_file(file_uuid: str):
    user_session_id = request.cookies.get("user_session_id")
    if not user_session_id:
        return Response(status=403)
    return send_from_directory(f".{PRELOAD_FOLDER}/{user_session_id}", file_uuid)
