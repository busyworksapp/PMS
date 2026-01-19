#!/bin/bash
# Railway startup script
# Properly handles environment variable expansion

PORT=${PORT:-8000}
export PYTHONUNBUFFERED=1

echo "Starting Barron PMS..."
echo "Port: $PORT"
echo "Debug: $DEBUG"

python -m uvicorn app.main:app \
  --host 0.0.0.0 \
  --port "$PORT" \
  --timeout-keep-alive 65 \
  --log-level info
