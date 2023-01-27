from dataclasses import dataclass

from fastapi import Depends

from app.database.repos.repo import Repo
from app.database.session_schema import repo_stub
from app.services.dishes_service import DishesService
from app.services.menu_service import MenuService
from app.services.submenu_service import SubmenuService


def service_stub():
    """
    Just DI for overwrite getting service

    :return: Nothing
    """
    raise NotImplementedError


@dataclass
class Services:
    menu_service: MenuService
    submenu_service: SubmenuService
    dishes_service: DishesService


def get_service(repo: Repo = Depends(repo_stub)):
    service = Services(
        menu_service=MenuService(repo.menu),
        submenu_service=SubmenuService(repo=repo.submenu, main_repo=repo),
        dishes_service=DishesService(repo=repo.dish, main_repo=repo),
    )

    yield service
