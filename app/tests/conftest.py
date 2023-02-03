import pytest_asyncio
from httpx import AsyncClient

from app.config.cfg import load_config
from main import get_app


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    """
    Pytest fixture for a AsyncClient

    :return: AsyncClient object
    """
    app = await get_app(load_config(".test.env"))

    async with AsyncClient(app=app, base_url="http://tester") as client:
        yield client
