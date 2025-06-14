from flask_migrate import Migrate  # type: ignore[import-untyped]
from flask_sqlalchemy import SQLAlchemy  # type: ignore[import-not-found]

db = SQLAlchemy()
db_migrate = Migrate()
