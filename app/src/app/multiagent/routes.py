from flask import Blueprint, jsonify, request, Response, stream_with_context  # type: ignore[import-not-found]  # isort: skip
from google.api_core.exceptions import ResourceExhausted  # type: ignore[import-not-found]  # isort: skip

from .agentrunnables import AgentRunnable

multi_agent_bp = Blueprint("multi_agent", __name__)


@multi_agent_bp.route("/chat", methods=["POST"])
def chat():
    try:
        payload = request.json
        runnable = AgentRunnable()

        def generate():
            for chunk in runnable.stream(
                question=payload["question"], agent_type=payload["agent"]
            ):
                yield chunk

        return Response(stream_with_context(generate()), mimetype="text/plain")
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
