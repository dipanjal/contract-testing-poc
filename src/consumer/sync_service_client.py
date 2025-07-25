import aiohttp
from typing import Dict, Any

# Alternative simpler version without context manager
class SimpleSyncServiceClient:
    """Simple async client without context manager requirements"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    async def get_version(self) -> Dict[str, Any]:
        """Get version information from sync-service"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/version") as response:
                response.raise_for_status()
                return await response.json()
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on sync-service"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/health") as response:
                response.raise_for_status()
                return await response.json()
