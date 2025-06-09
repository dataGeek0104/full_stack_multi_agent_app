from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def health_check():
    try:
        return jsonify({"message": "Yay! The app is working fine!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
