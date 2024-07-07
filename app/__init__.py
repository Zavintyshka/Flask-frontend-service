from flask import Flask

from .index import index_blueprint
from .user import user_blueprint
from .audio_service import audio_blueprint
from .video_service import video_blueprint
from .image_service import image_blueprint
from .middleware import middleware


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(audio_blueprint)
    app.register_blueprint(video_blueprint)
    app.register_blueprint(image_blueprint)
    middleware(app)

    return app
