from flask import Blueprint, jsonify, request  # type: ignore[import-not-found]  # isort: skip
from google.api_core.exceptions import ResourceExhausted  # type: ignore[import-not-found]  # isort: skip

from .agentrunnables import FinancialRunnable

multi_agent_bp = Blueprint("multi_agent", __name__)


@multi_agent_bp.route("/chat", methods=["POST"])
def signup():
    try:
        payload = request.json
        runnable = FinancialRunnable()
        response = runnable.run(question=payload["question"])
        return jsonify(response), 200
    except ResourceExhausted:
        return (
            jsonify(
                {
                    "error": "Oh no! Too many requests! Visit 'https://ai.google.dev/gemini-api/docs/rate-limits' for more information"
                }
            ),
            429,
        )
    except Exception as e:
        return jsonify({"error": e}), 500
