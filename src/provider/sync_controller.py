from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Version"])


class VersionResponse(BaseModel):
    service: str
    version: str
    build: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str


@router.get("/version", response_model=VersionResponse)
async def get_version() -> VersionResponse:
    """Get service version information"""
    return VersionResponse(
        service="sync-service",
        version="1.0.0",
        build="20240101-abc123",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )
