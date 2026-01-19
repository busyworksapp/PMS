FROM python:3.11-slim

WORKDIR /app

# Build timestamp: 2026-01-19 12:45:00 UTC
# Frontend files included in this build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY app/backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app/backend/app ./app

# Copy frontend files (HTML, CSS, JS)
COPY app/frontend ./frontend

# Copy entrypoint script
COPY entrypoint.py ./entrypoint.py

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run using Python entrypoint script to properly handle PORT environment variable
CMD ["python", "entrypoint.py"]
