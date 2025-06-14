import os

from app import app  # type: ignore[attr-defined, import-not-found]
from app.core import init_db_and_migrations  # type: ignore[import-not-found]

if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("BACKEND_PORT", "5010"))
    init_db_and_migrations(app)
    app.run(debug=True, port=port, host=host)
