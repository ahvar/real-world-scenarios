import os
from flask import Flask
from .main import bp as bp_main
from .api import bp as bp_api
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

base_dir = Path(__file__).parent.absolute()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{base_dir / 'data.sqlite'}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.register_blueprint(bp_main)

    app.register_blueprint(bp_api)

    return app
