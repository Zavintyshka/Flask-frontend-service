from flask import Blueprint

__all__ = ["video_blueprint"]

video_blueprint = Blueprint("video", __name__)


@video_blueprint.get("/video")
def start_video_page():
    return "Это стартовая страница видео-сервиса"
