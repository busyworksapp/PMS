#!/usr/bin/env python
"""
PMS Backend Server Startup Script
Keeps the server running continuously
"""
import subprocess
import sys
import time

def run_server():
    """Run the FastAPI server"""
    print("Starting Barron PMS Backend Server...")
    print("=" * 60)
    
    cmd = [
        sys.executable, 
        "-m", 
        "uvicorn", 
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--log-level", "info"
    ]
    
    try:
        process = subprocess.Popen(cmd)
        print(f"Server process started with PID: {process.pid}")
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Keep the process running
        while True:
            time.sleep(1)
            if process.poll() is not None:
                print(f"Server process exited with code: {process.returncode}")
                break
                
    except KeyboardInterrupt:
        print("\nShutting down server...")
        process.terminate()
        process.wait()
        print("Server stopped")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_server()
