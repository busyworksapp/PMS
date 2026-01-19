from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
import sys
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create app first to avoid circular imports
app = FastAPI(
    title="Barron Production Management System",
    description="Complete production management solution",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    try:
        # Import and initialize database with retries
        from app.db.database import Base, engine
        from sqlalchemy import text
        
        logger.info("Creating database tables...")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Test connection first
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                    logger.info("Database connection successful")
                
                # Create tables
                Base.metadata.create_all(bind=engine)
                logger.info("Database tables created successfully")
                break
            except Exception as db_error:
                if attempt < max_retries - 1:
                    logger.warning(f"Database connection attempt {attempt + 1} failed: {db_error}, retrying...")
                    import time
                    time.sleep(2)
                else:
                    logger.error(f"Database initialization failed after {max_retries} attempts: {db_error}")
                    # Don't raise - let the app start anyway so we can serve health checks
        
        # Import and register routes one by one
        logger.info("Importing routes...")
        
        try:
            from app.routes import auth
            logger.info("✓ Auth routes imported")
            app.include_router(auth.router)
        except Exception as e:
            logger.error(f"Auth routes error: {e}")
        
        try:
            from app.routes import master
            logger.info("✓ Master routes imported")
            app.include_router(master.router)
        except Exception as e:
            logger.error(f"Master routes error: {e}")
        
        try:
            from app.routes import orders
            logger.info("✓ Orders routes imported")
            app.include_router(orders.router)
        except Exception as e:
            logger.error(f"Orders routes error: {e}")
        
        try:
            from app.routes import defects
            logger.info("✓ Defects routes imported")
            app.include_router(defects.router)
        except Exception as e:
            logger.error(f"Defects routes error: {e}")
        
        try:
            from app.routes import maintenance
            logger.info("✓ Maintenance routes imported")
            app.include_router(maintenance.router)
        except Exception as e:
            logger.error(f"Maintenance routes error: {e}")
        
        try:
            from app.routes import sop_ncr
            logger.info("✓ SOP/NCR routes imported")
            app.include_router(sop_ncr.router)
        except Exception as e:
            logger.error(f"SOP/NCR routes error: {e}")
        
        try:
            from app.routes import jobs
            logger.info("✓ Jobs routes imported")
            app.include_router(jobs.router)
        except Exception as e:
            logger.error(f"Jobs routes error: {e}")
        
        try:
            from app.routes import job_planning
            logger.info("✓ Job planning routes imported")
            app.include_router(job_planning.router)
        except Exception as e:
            logger.error(f"Job planning routes error: {e}")
        
        try:
            from app.routes import finance
            logger.info("✓ Finance routes imported")
            app.include_router(finance.router)
        except Exception as e:
            logger.error(f"Finance routes error: {e}")
        
        try:
            from app.routes import whatsapp
            logger.info("✓ WhatsApp routes imported")
            app.include_router(whatsapp.router)
        except Exception as e:
            logger.error(f"WhatsApp routes error: {e}")
        
        # Mount static files (frontend)
        try:
            frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
            if os.path.exists(frontend_path):
                app.mount("/static", StaticFiles(directory=frontend_path), name="static")
                logger.info(f"✓ Frontend static files mounted from {frontend_path}")
        except Exception as e:
            logger.warning(f"Could not mount static files: {e}")
        
        logger.info("Application startup complete!")
        sys.stdout.flush()
        
    except Exception as e:
        logger.error(f"Fatal startup error: {e}", exc_info=True)
        raise


@app.get("/")
async def read_root():
    """Root endpoint - serves the login page."""
    try:
        # Try to serve the login HTML
        frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "login.html")
        if os.path.exists(frontend_path):
            return FileResponse(frontend_path, media_type="text/html")
    except Exception as e:
        logger.warning(f"Could not serve login.html: {e}")
    
    # Fallback to API info
    return {
        "message": "Barron Production Management System",
        "version": "1.0.0",
        "status": "operational",
        "api_docs": "/docs",
        "health_check": "/health",
        "endpoints": {
            "authentication": "/api/auth/register",
            "whatsapp": "/api/whatsapp/send",
            "orders": "/api/orders",
            "masters": "/api/master",
            "defects": "/api/defects",
            "maintenance": "/api/maintenance",
            "jobs": "/api/jobs",
            "finance": "/api/finance"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Frontend page routes
@app.get("/login")
async def login_page():
    """Serve login page."""
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "login.html")
        if os.path.exists(frontend_path):
            return FileResponse(frontend_path, media_type="text/html")
    except Exception as e:
        logger.warning(f"Could not serve login.html: {e}")
    return {"error": "Login page not found"}


@app.get("/dashboard")
async def dashboard_page():
    """Serve dashboard page."""
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dashboard.html")
        if os.path.exists(frontend_path):
            return FileResponse(frontend_path, media_type="text/html")
    except Exception as e:
        logger.warning(f"Could not serve dashboard.html: {e}")
    return {"error": "Dashboard page not found"}


@app.get("/admin")
async def admin_page():
    """Serve admin page."""
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "admin.html")
        if os.path.exists(frontend_path):
            return FileResponse(frontend_path, media_type="text/html")
    except Exception as e:
        logger.warning(f"Could not serve admin.html: {e}")
    return {"error": "Admin page not found"}


@app.get("/orders")
async def orders_page():
    """Serve orders page."""
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "order-list.html")
        if os.path.exists(frontend_path):
            return FileResponse(frontend_path, media_type="text/html")
    except Exception as e:
        logger.warning(f"Could not serve order-list.html: {e}")
    return {"error": "Orders page not found"}


@app.get("/maintenance")
async def maintenance_page():
    """Serve maintenance page."""
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "maintenance.html")
        if os.path.exists(frontend_path):
            return FileResponse(frontend_path, media_type="text/html")
    except Exception as e:
        logger.warning(f"Could not serve maintenance.html: {e}")
    return {"error": "Maintenance page not found"}
