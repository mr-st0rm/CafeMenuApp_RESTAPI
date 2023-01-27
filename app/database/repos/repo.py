from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from .dishes_repo import DishesRepo
from .menu_repo import MenuRepo
from .sub_menu_repo import SubMenuRepo


class Repo:
    menu: MenuRepo
    submenu: SubMenuRepo
    dish: DishesRepo

    def __init__(
            self,
            session: AsyncSession,
            menu: Type[MenuRepo],
            submenu: Type[SubMenuRepo],
            dish: Type[DishesRepo]
    ):
        self.menu = menu(session)
        self.submenu = submenu(session)
        self.dish = dish(session)
