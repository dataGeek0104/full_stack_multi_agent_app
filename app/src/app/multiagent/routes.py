from flask import Blueprint, jsonify  # type: ignore[import-not-found]  # isort: skip


multi_agent_bp = Blueprint("multi_agent", __name__)


@multi_agent_bp.route("/chat", methods=["GET"])
def signup():
    return jsonify({"message": "Yay! The chat is working fine!"}), 200
