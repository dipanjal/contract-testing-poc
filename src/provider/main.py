import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from src.provider import (
    sync_controller,
    provider_state_controller
)

# ────────────────────────────────────────────────────────────────────────────────
# Logging
# ────────────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
PROVIDER_DIR = str(Path(__file__).parent.resolve())

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
app.include_router(provider_state_controller.router)

# running uvicorn as a simple python server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        reload_dirs=[PROVIDER_DIR]
    )

# Alternatively, you can use to run the server from the command line or from a bash script like this
# uvicorn ./src/provider/main:app --host=0.0.0.0 --port=5000 --reload-dir=./src/provider --reload
