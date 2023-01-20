import configparser
import os

from pydantic.dataclasses import dataclass


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
class AppConfig:
    app: FastApiApp
    db: DataBase


def load_config(cfg_path: str = "cfg.ini") -> AppConfig:
    """
    Load and parse config from .ini config file

    :param cfg_path: path to config file
    :return: AppConfig object
    """
    cfg_path = os.getenv("CONFIG_FILE") or cfg_path
    config = configparser.ConfigParser()
    config.read(cfg_path)

    return AppConfig(
        app=FastApiApp(**config["app"]),
        db=DataBase(**config["db"])
    )
