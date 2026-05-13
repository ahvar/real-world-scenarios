from flask import Flask
from app.main import bp as main_bp


def create_app():
    app = Flask(__name__)
    from app.main import bp as bp_main

    app.register_blueprint(bp_main)

    return app
