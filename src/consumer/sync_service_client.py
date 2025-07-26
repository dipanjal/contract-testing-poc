import aiohttp
from typing import Dict, Any

from pydantic import BaseModel


class VersionResponse(BaseModel):
    service: str
    version: str
    build: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str

# Alternative simpler version without context manager
class SimpleSyncServiceClient:
    """Simple async client without context manager requirements"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    async def get_version(self) -> VersionResponse:
        """Get version information from sync-service"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/version") as response:
                response.raise_for_status()
                data = await response.json()
                return VersionResponse(**data)
    
    async def health_check(self) -> HealthResponse:
        """Perform health check on sync-service"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/health") as response:
                response.raise_for_status()
                data = await response.json()
                return HealthResponse(**data)
