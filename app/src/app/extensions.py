import os

from flask_migrate import Migrate  # type: ignore[import-untyped]
from flask_sqlalchemy import SQLAlchemy  # type: ignore[import-not-found]
from sqlalchemy import event, text  # type: ignore[import-not-found]

db = SQLAlchemy()
db_migrate = Migrate()


@event.listens_for(db.metadata, "before_create")
def _create_schema_before_create(target, connection, **_kw) -> None:
    """Ensure the configured schema exists before table creation."""
    schema = os.getenv("POSTGRES_SCHEMA")
    if schema:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
