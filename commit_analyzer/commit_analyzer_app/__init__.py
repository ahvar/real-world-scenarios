from flask import Flask
from dotenv import load_dotenv
from pathlib import Path
from config import Config

base_dir = Path(__file__).parent
env_dir = base_dir / ".env"

load_dotenv(env_dir)


def create_app():
    app = Flask(__name__)
    return app
