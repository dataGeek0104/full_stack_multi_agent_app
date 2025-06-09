import pytest
from flask import Flask
from src.app.core.routes import api_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert (
        response.status_code == 200
    )  # Optional: use `assert response.status_code == 200  # nosec`
    assert response.json == {"message": "Yay! The app is working fine!"}  # nosec
