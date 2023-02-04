from sqlalchemy.ext.asyncio import AsyncSession

from .dishes_repo import DishesRepo
from .grab_db_repo import GrabberDBRepo
from .menu_repo import MenuRepo
from .redis_repo import RedisRepo
from .sub_menu_repo import SubMenuRepo


class Repo:
    menu: MenuRepo
    submenu: SubMenuRepo
    dish: DishesRepo
    grabber: GrabberDBRepo
    redis: RedisRepo

    def __init__(
        self,
        session: AsyncSession,
        menu: type[MenuRepo],
        submenu: type[SubMenuRepo],
        dish: type[DishesRepo],
        grabber: type[GrabberDBRepo],
    ):
        self.menu = menu(session)
        self.submenu = submenu(session)
        self.dish = dish(session)
        self.grabber = grabber(session)
