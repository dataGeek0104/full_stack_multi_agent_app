import os
from typing import Optional

import jwt  # type: ignore[import-not-found]
from flask import Flask  # type: ignore[import-not-found]
from flask import Blueprint, current_app, g, jsonify, request
from sqlalchemy import text  # type: ignore[import-not-found]

from ..core.routes import core_bp  # type: ignore[import-not-found]
from ..extensions import db, db_migrate  # type: ignore[import-not-found]
from ..user.routes import user_bp  # type: ignore[import-not-found]

from flask_migrate import init, migrate, upgrade  # type: ignore[import-untyped]  # isort: skip


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
    api_v0.register_blueprint(user_bp, url_prefix="user")

    # Register the global blueprint with the app
    app.register_blueprint(api_v0)

    @app.before_request
    def authenticate() -> Optional[tuple]:
        public_endpoints = {
            "api_v0.core.health_check",
            "api_v0.core.db_conn_check",
            "api_v0.user.signup",
            "api_v0.user.login",
        }

        if request.endpoint in public_endpoints:
            return  # type: ignore[return-value]

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401
        token = auth_header.split("Bearer ")[1]
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            g.username = payload.get("username")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return None

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
