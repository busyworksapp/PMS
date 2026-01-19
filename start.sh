#!/bin/sh
# Railway startup script
# Properly handles environment variable expansion

PORT=${PORT:-8000}
export PYTHONUNBUFFERED=1

echo "Starting Barron PMS on port $PORT..."

exec python -m uvicorn app.main:app \
  --host 0.0.0.0 \
  --port "$PORT" \
  --timeout-keep-alive 65 \
  --log-level info
