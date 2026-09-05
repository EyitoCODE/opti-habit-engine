"""
Opti-Habit Engine: Main API Application Entrypoint

Initializes FastAPI middleware, builds database tables,
registers API route blueprints, and mounts static dashboard assets.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes import router as habit_router
from db.database import engine, Base

# Build all declared database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Opti-Habit Engine API",
    description="Algorithmic habit tracker pairing EMA momentum with OpenCV hardware verification.",
    version="1.0.0"
)

# Cross-Origin Resource Sharing configuration for decoupled web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route blueprints
app.include_router(habit_router)

@app.get("/health")
def health_check():
    """Confirms operational status of the service."""
    return {"status": "Algorithmic Engine & API Online"}

# Mount frontend directory for direct UI serving
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.isdir(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")