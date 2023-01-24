import pytest_asyncio
from httpx import AsyncClient

from app.config.cfg import load_config
from main import get_app


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    app = await get_app(load_config('.test.env'))

    async with AsyncClient(app=app) as client:
        yield client
