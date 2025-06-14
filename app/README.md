# Backend for Full-stack Multi-agent Application

This backend handles the logic for autonomous agents and interacts with the PostgreSQL database. The backend is run entirely inside Docker.

---

## 🐳 Docker-First Development

### 🧱 Base Image

```Dockerfile
FROM python:3.9-slim
```

All dependencies and services are installed via `poetry`.

---

## 📁 Directory Structure

- `src/` - Source code
- `tests/` - Pytest-based tests
- `alembic.ini` - DB migrations
- `pyproject.toml` - Project config
- `Dockerfile` - Backend container build

---

## 🐘 Database Connection

Configured via `.env`:

```env
SECRET_KEY=<your_secret_key>
POSTGRES_HOST="pglgma"
POSTGRES_PORT=5432
POSTGRES_DB="<your_postgres_db>"
POSTGRES_USER="<your_postgres_user>"
POSTGRES_PASSWORD="<your_postgres_password>"
POSTGRES_SCHEMA="lgma"
SQLALCHEMY_DATABASE_URI="postgresql://<your_postgres_db>:<your_postgres_password>@pglgma:5432/<your_postgres_db>"
```

(Ensure that you replace `<your_secret_key>` with your own secret-key and `<your_postgres_user>`, `<your_postgres_password>` and `<your_postgres_db>` with your actual postersql connection configurations.)

---
