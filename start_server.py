from flask import render_template, request
from app import create_app

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    print(request.url)
    print(e)
    return render_template("errors/page_not_found.html"), 404
