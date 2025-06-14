# Use official Python 3.9 base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.7.1
RUN curl -sSL https://install.python-poetry.org | python3.9 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy only the poetry files to install dependencies first (cache optimization)
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create true \
    && poetry install --no-interaction --no-ansi --no-root \
    && poetry self add poetry-dotenv-plugin

# Copy the rest of the app
COPY . .

RUN poetry install --no-interaction --no-ansi \
    && poetry install --with dev

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (adjust if using FastAPI or Flask)
EXPOSE 5010

# Default command (adjust if different app entry point)
CMD ["poetry", "run", "python", "-m", "src.run"]
