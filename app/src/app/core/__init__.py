import os

from flask import Blueprint, Flask  # type: ignore[import-not-found]
from flask_migrate import init  # type: ignore[import-untyped]
from flask_migrate import migrate, upgrade
from sqlalchemy import text  # type: ignore[import-not-found]

from ..core.routes import core_bp  # type: ignore[import-not-found]
from ..extensions import db, db_migrate  # type: ignore[import-not-found]

from app.user.models import User  # type: ignore[import-not-found]  # noqa: F401  # isort: skip


def create_app():
    app = Flask(__name__)

    # Config from environment
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    db_migrate.init_app(app, db)

    # Register routes
    api_v0 = Blueprint("api_v0", __name__, url_prefix="/api/v0")
    api_v0.register_blueprint(core_bp, url_prefix="")

    # Register the global blueprint with the app
    app.register_blueprint(api_v0)

    return app


def init_db_and_migrations(app):
    with app.app_context():
        schema = os.getenv("POSTGRES_SCHEMA", "lgma")
        with db.engine.begin() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))

        if not os.path.isdir("migrations"):
            init()
            migrate(message="Initial migration.")

        upgrade()
