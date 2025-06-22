import os
from datetime import datetime

from ..extensions import db  # type: ignore[import-not-found]

from werkzeug.security import check_password_hash  # type: ignore[import-not-found]  # isort: skip


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {
        "schema": os.getenv("POSTGRES_SCHEMA", "lgma"),
        "extend_existing": True,
    }

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
