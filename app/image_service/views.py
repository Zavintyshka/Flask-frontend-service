from flask import Blueprint

__all__ = ["image_blueprint"]

image_blueprint = Blueprint("image", __name__)


@image_blueprint.get("/image")
def image_start_page():
    return "Это стартовая страница сервиса для редактирования фото"
