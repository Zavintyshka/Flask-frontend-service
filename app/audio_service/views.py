from flask import Blueprint, render_template, g

__all__ = ["audio_blueprint"]

audio_blueprint = Blueprint("audio", __name__)


@audio_blueprint.get('/audio')
def audio_start_page():
    return render_template("audio/audio_index.html", **g.user)
