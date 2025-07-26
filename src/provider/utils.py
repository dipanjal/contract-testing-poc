"""Utility functions for provider tests."""
import asyncio
import subprocess
from contextlib import asynccontextmanager

import aiohttp

from src.provider.constants import SELF_HOST_URL


class ServerManager:
    process = None

    @classmethod
    async def start_server(cls):
        if cls.process:
            raise RuntimeError("Server is already running PID %s", cls.process.pid)
        print("Starting Server...")
        cls.process = subprocess.Popen(["python", "main.py"])
        await asyncio.sleep(3)  # Wait for server to start

    @classmethod
    def stop_server(cls):
        if cls.process:
            print("Stopping Server...")
            cls.process.terminate()
            cls.process = None

async def check_version_http_status() -> int:
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(f"{SELF_HOST_URL}/version") as response:
            return response.status

@asynccontextmanager
async def service_running(autorun=False, max_retry=3):
    """Async context manager to validate if the provider service is running at SELF_HOST_URL."""
    count = 0
    max_retry = 1 if max_retry <= 0 else max_retry

    while count < max_retry:
        try:
            if autorun and count > 0:
                await ServerManager.start_server()
            status = await check_version_http_status()
            if status == 200:
                yield
                return
        except Exception as e:
            if not autorun or (count + 1) == max_retry:
                raise Exception(f"Provider service at {SELF_HOST_URL} is not running or not accessible: {str(e)}")
        finally:
            ServerManager.stop_server()
        count += 1