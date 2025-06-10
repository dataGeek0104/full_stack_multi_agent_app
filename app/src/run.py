import os

from src.app import app

if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("BACKEND_PORT", "5001"))
    app.run(debug=True, port=port, host=host)
