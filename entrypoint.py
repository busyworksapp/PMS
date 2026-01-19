#!/usr/bin/env python3
"""
Railway startup wrapper
Properly handles environment variable expansion for PORT
"""
import os
import subprocess
import sys

PORT = os.getenv("PORT", "8000")

print(f"Starting Barron PMS on port {PORT}")
print(f"Python: {sys.executable}")

# Build the uvicorn command
cmd = [
    sys.executable,
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    PORT,
    "--timeout-keep-alive",
    "65",
    "--log-level",
    "info",
]

print(f"Command: {' '.join(cmd)}")

# Replace this process with uvicorn
os.execvp(sys.executable, cmd)
