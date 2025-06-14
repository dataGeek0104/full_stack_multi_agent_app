import os

import pytest  # type: ignore[import-not-found]
from flask import Flask  # type: ignore[import-not-found]

from app.core.routes import core_bp  # type: ignore[import-not-found]
from app.extensions import db  # type: ignore[import-not-found]


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(core_bp)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health-check")
    assert response.status_code == 200  # nosec
    assert response.json == {"message": "Yay! The app is working fine!"}  # nosec


def test_db_conn_check(client):
    response = client.get("/db-conn-check")
    assert response.json == {"message": "Yay! The DB is working fine!"}  # nosec
    assert response.status_code == 200  # nosec
