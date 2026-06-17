FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FASTAPI_ENV=production \
    PYTHONPATH=/app \
    UV_PROJECT_ENVIRONMENT=/app/.venv  

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Create user early
RUN useradd -m appuser

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-build

# Copy application code
COPY . .

# Fix ownership
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD ["uv", "run", "--frozen", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]