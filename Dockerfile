FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY app/backend/requirements.txt ./backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend code
COPY app/backend/app ./backend/app

# Expose port
EXPOSE 8000

# Set working directory
WORKDIR /app/backend

# Run uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
