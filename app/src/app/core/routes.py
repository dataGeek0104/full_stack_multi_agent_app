from flask import Blueprint, jsonify  # type: ignore[import-not-found]
from sqlalchemy import text  # type: ignore[import-not-found]

from ..extensions import db  # type: ignore[import-not-found]

core_bp = Blueprint("core", __name__)


@core_bp.route("/health-check", methods=["GET"])
def health_check():
    try:
        return jsonify({"message": "Yay! The app is working fine!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@core_bp.route("/db-conn-check", methods=["GET"])
def db_conn_check():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"message": "Yay! The DB is working fine!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
