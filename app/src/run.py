import os

from app import app  # type: ignore[attr-defined]

if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("BACKEND_PORT", "5001"))
    app.run(debug=True, port=port, host=host)
