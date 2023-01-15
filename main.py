import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.api import register_api_routes
from app.config.cfg import DataBase, AppConfig, load_config
from app.database import get_engine
from app.database.models import BaseModel
from app.database.session_schema import DBProvider, repo_stub


async def init_models(db: DataBase):
    """ Create all tables in database """
    engine: AsyncEngine = get_engine(db)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


def get_app(cfg: AppConfig) -> FastAPI:
    """
    Main function for configure FastAPI application

    :param cfg: AppConfig object
    :return: FastAPI configured object
    """
    application = FastAPI()

    asyncio.run(init_models(cfg.db))

    #  Database 'async' engine and sessionmaker object
    engine = get_engine(cfg.db)
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    provider = DBProvider(db_pool)

    # DI in order to overturn the repository and ensure the independence of the handler from creation of the repository
    application.dependency_overrides[repo_stub] = provider.get_repo

    #  register CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_api_routes(application)

    return application


if __name__ == "__main__":
    try:
        config = load_config()
        app = get_app(config)

        uvicorn.run(app, host=config.app.host, port=config.app.port)
    except (SystemError, KeyboardInterrupt):
        logging.error("Application shutdown")