from flask import Flask
from routes import bp as route_bp


def create_app():

    app = Flask(__name__)
    app.register_blueprint(route_bp)
    return app
