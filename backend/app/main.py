from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.database import init_db
from app.routers import auth_router, sweets_router

# Initialize FastAPI app
app = FastAPI(
    title="Sweet Shop Management System API",
    description="A RESTful API for managing a sweet shop with authentication and inventory",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router)
app.include_router(sweets_router.router)

@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    init_db()

@app.get("/", tags=["root"])
def root():
    """Root endpoint - API health check"""
    return {
        "message": "Sweet Shop Management System API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
