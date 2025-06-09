import os

from dotenv import load_dotenv  # type: ignore[import-not-found]
from flask import Flask  # type: ignore[import-not-found]
from src.app.core.routes import api_bp
from src.app.extensions import db


def create_app():
    load_dotenv()  # Load environment variables from .env

    app = Flask(__name__)

    # Config from environment
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Register routes
    app.register_blueprint(api_bp, url_prefix="/api/v0")

    db.init_app(app)

    return app
