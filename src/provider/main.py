"""
Application entry point for the sync-service
"""


from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging

# Import controllers
import provider_state_controller, sync_controller

# ────────────────────────────────────────────────────────────────────────────────
# Logging
# ────────────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────────────────────────
# Lifespan
# ────────────────────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup
    print("Server listening...")
    yield
    # Shutdown
    print("Shutting down...")

# ────────────────────────────────────────────────────────────────────────────────
# FastAPI app
# ────────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="User Management API",
    description="A FastAPI application with MySQL using raw SQL queries and layered architecture",
    version="1.0.0",
    lifespan=lifespan
)

# ────────────────────────────────────────────────────────────────────────────────
# Include routers
# ────────────────────────────────────────────────────────────────────────────────
app.include_router(sync_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
