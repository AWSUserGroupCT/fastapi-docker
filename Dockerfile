# 1. Builder Stage
FROM python:3.15-slim AS builder

# Install uv from the official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation for faster startup
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies only (exclude dev dependencies)
RUN uv sync --frozen --no-dev --no-install-project

# Copy application source code
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev

# 2. Runtime Stage
FROM python:3.12-slim

WORKDIR /app

# Create a non-root user for security
RUN groupadd --system app && useradd --system --gid app --no-create-home app

# Copy the uv-managed Python interpreter (the venv symlinks to it)
COPY --from=builder /python /python

# Copy the virtual environment and code from the builder
COPY --from=builder --chown=app:app /app /app

# Add the virtual environment's bin directory to the PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Switch to the non-root user
USER app

# Expose the port
EXPOSE 8000

# Run the FastAPI application
# 'fastapi run' is recommended for production over 'fastapi dev'
CMD ["fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]   