FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        python3-pip \
        python3-amqp \
        python3-setuptools \
    && pip3 install --break-system-packages rabbitmq-admin \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - \
    && poetry --version \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
RUN poetry install --no-root --only main

COPY src/ ./src/
WORKDIR /app/src

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
