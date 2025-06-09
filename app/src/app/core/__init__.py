import os

from dotenv import load_dotenv
from flask import Flask

from app.core.routes import api_bp


def create_app():
    load_dotenv()  # Load environment variables from .env

    app = Flask(__name__)

    # Config from environment
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Register routes
    app.register_blueprint(api_bp, url_prefix="/api/v0")

    return app
