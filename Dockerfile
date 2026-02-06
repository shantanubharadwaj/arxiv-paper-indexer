FROM python:3.12.8-slim AS base

WORKDIR /app

# Install system dependencies if needed (for psycopg2-binary, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt ./

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src /app/src

FROM python:3.12.8-slim AS final

EXPOSE 8000

# PYTHONUNBUFFERED=1 to disable output buffering
ENV PYTHONUNBUFFERED=1
ARG VERSION=0.1.0
ENV APP_VERSION=$VERSION

WORKDIR /app

# Copy installed packages and source from base stage
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /app/src /app/src

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]