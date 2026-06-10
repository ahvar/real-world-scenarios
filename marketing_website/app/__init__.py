from flask import Flask
from api import bp as api_bp
from main import bp as main_bp


def create_app():

    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    return app
