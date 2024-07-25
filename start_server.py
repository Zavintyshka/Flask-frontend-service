from flask import render_template, request
from app import create_app

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    print(request.url)
    print(e)
    return render_template("errors/standard_error_page.html", message="Page not Found. 404"), 404
