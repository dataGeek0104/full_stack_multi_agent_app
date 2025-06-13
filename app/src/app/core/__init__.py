import os

from dotenv import load_dotenv  # type: ignore[import-not-found]
from flask import Blueprint, Flask  # type: ignore[import-not-found]

from app.core.routes import core_bp  # type: ignore[import-not-found]
from app.extensions import db  # type: ignore[import-not-found]


def create_app():
    load_dotenv()  # Load environment variables from .env

    app = Flask(__name__)

    # Config from environment
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Register routes
    api_v0 = Blueprint("api_v0", __name__, url_prefix="/api/v0")
    api_v0.register_blueprint(core_bp, url_prefix="")

    # Register the global blueprint with the app
    app.register_blueprint(api_v0)

    db.init_app(app)

    return app
