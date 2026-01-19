from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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

# Import models and routes after app creation
from app.db.database import Base, engine
from app.routes import auth, master, orders, defects
from app.routes import maintenance, sop_ncr, jobs, whatsapp
from app.routes import job_planning, finance

# Initialize database tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization warning: {e}")

# Register all routers
app.include_router(auth.router)
app.include_router(master.router)
app.include_router(orders.router)
app.include_router(jobs.router)
app.include_router(job_planning.router)
app.include_router(defects.router)
app.include_router(maintenance.router)
app.include_router(sop_ncr.router)
app.include_router(finance.router)
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
