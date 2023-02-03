from dataclasses import dataclass

from aioredis import Redis
from fastapi import Depends

from app.database.redis_cache import redis_stub
from app.database.repos.redis_repo import RedisRepo
from app.database.repos.repo import Repo
from app.database.session_schema import repo_stub
from app.services.dishes_service import DishesService
from app.services.menu_service import MenuService
from app.services.submenu_service import SubmenuService


def service_stub():
    """Just DI for overwrite getting service"""
    raise NotImplementedError


@dataclass
class Services:
    menu_service: MenuService
    submenu_service: SubmenuService
    dishes_service: DishesService


def get_service(
    repo: Repo = Depends(repo_stub), redis: Redis = Depends(redis_stub)
):
    redis = RedisRepo(redis)

    service = Services(
        menu_service=MenuService(main_repo=repo, redis=redis),
        submenu_service=SubmenuService(main_repo=repo, redis=redis),
        dishes_service=DishesService(main_repo=repo, redis=redis),
    )

    yield service
