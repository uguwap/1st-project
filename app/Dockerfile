# Stage 1: Сборка зависимостей
FROM python:3.12-slim AS builder
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv

ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Копируем только файлы зависимостей
COPY ./app/pyproject.toml ./app/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Копируем код приложения
COPY ./app /app/backend
COPY ./migrations /app/migrations
COPY ./.env /app/

# Stage 2: Миграции
FROM python:3.12-slim AS migrations
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/backend /app/backend
COPY --from=builder /app/migrations /app/migrations
COPY --from=builder /app/.env /app/.env
COPY --from=builder /app/migrations/alembic.ini /app/migrations/alembic.ini

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:/app/backend"
ENV ALEMBIC_CONFIG=/app/migrations/alembic.ini
CMD ["alembic", "upgrade", "head"]

# Stage 3: Development
FROM python:3.12-slim AS dev
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/backend /app/backend
COPY --from=builder /app/migrations /app/migrations
COPY --from=builder /app/.env /app/.env

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:/app/backend"
ENV ALEMBIC_CONFIG=/app/migrations/alembic.ini
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 4: Production
FROM python:3.12-slim AS prod
WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/backend /app/backend
COPY --from=builder /app/.env /app/.env

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:/app/backend"
ENV ALEMBIC_CONFIG=/app/migrations/alembic.ini
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

