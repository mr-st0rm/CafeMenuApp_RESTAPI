import os
from dataclasses import dataclass

import environs


@dataclass
class FastApiApp:
    host: str
    port: int


@dataclass
class DataBase:
    host: str
    port: int
    user: str
    password: str
    db_name: str


@dataclass
class RedisCache:
    host: str
    port: int
    db_id: int


@dataclass
class CeleryApp:
    broker_url: str
    result_backend: str


@dataclass
class AppConfig:
    app: FastApiApp
    db: DataBase
    redis: RedisCache
    celery: CeleryApp


def load_config(cfg_path: str = ".prod.env") -> AppConfig:
    """
    Load and parse config from .env config file

    :param cfg_path: path to config file
    :return: AppConfig object
    """
    env = environs.Env()
    cfg_path = os.getenv("CONFIG_FILE") or cfg_path
    env.read_env(cfg_path)

    return AppConfig(
        app=FastApiApp(
            host=env.str("HOST"),
            port=env.str("PORT"),
        ),
        db=DataBase(
            host=env.str("PG_HOST"),
            port=env.int("PG_PORT"),
            user=env.str("POSTGRES_USER"),
            password=env.str("POSTGRES_PASSWORD"),
            db_name=env.str("POSTGRES_DB"),
        ),
        redis=RedisCache(
            host=env.str("RS_HOST"),
            port=env.int("RS_PORT"),
            db_id=env.int("RS_DB"),
        ),
        celery=CeleryApp(
            broker_url=env.str("C_BROKER_URL"),
            result_backend=env.str("C_RESULT_BACKEND"),
        ),
    )
