"""
Barron Production Management System
FastAPI Application Entry Point

This is the main application that initializes all routes,
middleware, and database connections.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
