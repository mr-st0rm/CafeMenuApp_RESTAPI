import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient() as client:
        yield client
