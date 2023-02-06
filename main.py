import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.api import register_api_routes
from app.config.cfg import AppConfig, DataBase, load_config
from app.database import get_engine
from app.database.models import BaseModel
from app.database.redis_cache import RedisProvider, redis_stub
from app.database.session_schema import DBProvider, repo_stub
from app.services.service import get_service, service_stub


async def init_models(db: DataBase):
    """
    Create all tables in database

    :param db: DB config class
    """
    engine: AsyncEngine = get_engine(db)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


application = FastAPI()


async def get_app(cfg: AppConfig) -> FastAPI:
    """
    Main function for configure FastAPI application

    :param cfg: AppConfig object
    :return: FastAPI configured object
    """
    global application

    await init_models(cfg.db)

    #  Database 'async' engine and sessionmaker object
    engine = get_engine(cfg.db)
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    repo_provider = DBProvider(db_pool)
    redis = RedisProvider(cfg.redis)

    # DI in order to overturn the repository and ensure the independence
    # of the handler from creation of the repository
    application.dependency_overrides[repo_stub] = repo_provider.get_repo
    application.dependency_overrides[service_stub] = get_service
    application.dependency_overrides[redis_stub] = redis.get_redis

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
        asyncio.run(get_app(config))

        uvicorn.run(application, host=config.app.host, port=config.app.port)
    except (SystemError, KeyboardInterrupt):
        logging.error("Application shutdown")
