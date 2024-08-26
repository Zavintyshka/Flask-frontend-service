from flask import render_template, request, Response
from flask_wtf import CSRFProtect
from app import create_app
from settings import settings

app = create_app()
app.secret_key = settings.FLASK_SECRET_KEY
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
csrf = CSRFProtect(app)


@app.after_request
def apply_csp(response: Response):
    if "text/html" in response.headers["Content-Type"]:
        response.headers["Content-Security-Policy"] = "script-src 'self' cdn.jsdelivr.net"
    return response


@app.errorhandler(404)
def page_not_found(e):
    print(request.url)
    print(e)
    return render_template("errors/standard_error_page.html", message="Page not Found. 404"), 404
