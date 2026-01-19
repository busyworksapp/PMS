from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    """Initialize database tables on demand."""
    from app.db.database import Base, engine
    
    # Create tables
    Base.metadata.create_all(bind=engine)


# Create app first to minimize SQLAlchemy load issues
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


def register_routes():
    """Register routes after app is initialized."""
    from app.routes import auth, master, orders, defects
    from app.routes import maintenance, sop_ncr, jobs, whatsapp
    
    app.include_router(auth.router)
    app.include_router(master.router)
    app.include_router(orders.router)
    app.include_router(jobs.router)
    app.include_router(defects.router)
    app.include_router(maintenance.router)
    app.include_router(sop_ncr.router)
    app.include_router(whatsapp.router)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Barron Production Management System",
        "api_docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    """Initialize routes on startup (database initialization is deferred)."""
    try:
        register_routes()
    except Exception:
        # Routes already registered, ignore on reload
        pass
