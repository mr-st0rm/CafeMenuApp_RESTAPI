from sqlalchemy.ext.asyncio import AsyncSession

from .dishes_repo import DishesRepo
from .menu_repo import MenuRepo
from .redis_repo import RedisRepo
from .sub_menu_repo import SubMenuRepo


class Repo:
    menu: MenuRepo
    submenu: SubMenuRepo
    dish: DishesRepo
    redis: RedisRepo

    def __init__(
        self,
        session: AsyncSession,
        menu: type[MenuRepo],
        submenu: type[SubMenuRepo],
        dish: type[DishesRepo],
    ):
        self.menu = menu(session)
        self.submenu = submenu(session)
        self.dish = dish(session)
