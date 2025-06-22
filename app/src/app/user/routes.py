from datetime import datetime, timedelta

import jwt  # type: ignore[import-not-found]
from sqlalchemy.exc import SQLAlchemyError  # type: ignore[import-not-found]

from ..extensions import db
from .models import User

from flask import Blueprint, current_app, jsonify, request  # type: ignore[import-not-found]  # isort: skip
from werkzeug.security import generate_password_hash  # type: ignore[import-not-found]  # isort: skip


user_bp = Blueprint("user", __name__)


@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "user already exists", "username": username}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return (
        jsonify({"message": "User created", "username": username}),
        201,
    )


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    payload = {
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(days=1),
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    payload["token"] = token

    return jsonify(payload), 200
