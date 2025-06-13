# Full-stack Multi-agent Application

This project is a **Docker-native full-stack application** that leverages autonomous agents running in a Python backend, managed through Docker Compose. It also integrates PostgreSQL as a database and uses Alembic for migrations.

---

## 🧱 Architecture Overview

This app consists of:

- **Backend (Flask/FastAPI/WSGI)** service container
- **PostgreSQL** database container
- All components are fully orchestrated using **Docker Compose**

---

## 🐳 Docker Compose Setup

### 📦 Services Defined

```yaml
- backend
- db
```

### 🛠️ Environment Variables (from `.env`)

```env
HOST=0.0.0.0
BACKEND_PORT=5001
PORT=3001
POSTGRES_USER=<your_postgres_user>
POSTGRES_PASSWORD=<your_postgres_password>
POSTGRES_DB=<your_postgres_db>
DATABASE_URL=postgresql://<your_postgres_user>:<your_postgres_password>@localhost:5432/<your_postgres_db>
```

(Ensure that you replace `<your_postgres_user>`, `<your_postgres_password>` and `<your_postgres_db>` with your actual postersql connection configurations.)

---

## 🚀 Quick Start

- **Build and start all services**

```bash
docker compose up --build
```

- **Check the application**
  - App health check:

    ```bash
    curl -X GET "http://localhost:5001/api/v0/health-check"
    ```

    Output:

    ```bash
    {
    "message": "Yay! The app is working fine!"
    }
    ```

  - Database connection check:

    ```bash
    curl -X GET "http://localhost:5001/api/v0/db-conn-check"
    ```

    Output:

    ```bash
    {
    "message": "Yay! The DB is working fine!"
    }
    ```

---

## ✅ Running Tests

Run all tests inside the container:

```bash
docker compose exec backend pytest
```

---

## 📁 Project Structure

- `compose.yaml`: Docker service composition
- `.env`: Environment configuration
- `app/`: Python backend source code containing the agent runtime and services.
- `.github/` - CI/CD workflows and automation scripts.

---
