import sqlalchemy.orm
from sqlalchemy.ext.asyncio import create_async_engine

from app.config.cfg import DataBase


def make_connection_string(db: DataBase, async_fallback: bool = False) -> str:
    """
    Generate a connection string to DataBase

    :param db: config data
    :param async_fallback: fallback flag
    :return: string
    """
    result = f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.db_name}"
    if async_fallback:
        result += "?async_fallback=True"
    return result


def get_engine(db: DataBase) -> sqlalchemy.ext.asyncio.AsyncEngine:
    """
    Create async engine to database

    :param db: config data
    :return: AsyncEngine
    """
    engine: sqlalchemy.ext.asyncio.AsyncEngine = create_async_engine(
        make_connection_string(db), encoding="utf-8", echo=False, future=True
    )

    return engine
