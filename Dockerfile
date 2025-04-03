FROM python:3.12-slim AS base

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy project files and install dependencies
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-dev

# Add the virtual environment's bin directory to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

