from sqlalchemy import select

from app.database.models import Menus
from app.database.repos import SQLAlchemyRepo


class MenuRepo(SQLAlchemyRepo):
    async def _get_menu(self, menu_id: int) -> Menus | None:
        """
         Get menu by PK from Menus table

        :param menu_id: target menu id
        :return: Dish object or None
        """
        menu = await self.session.get(Menus, menu_id)

        return menu

    async def menu_info(self, menu_id: int) -> Menus | None:
        """
        Get Menu object by id

        :param menu_id: id of target menu
        :return: Menu object or None
        """
        menu = await self._get_menu(menu_id)

        return menu

    async def get_all_menus(self) -> list[Menus]:
        """
        Get list of all menus

        :return: list of Menu objects
        """
        smtp = select(Menus).order_by(Menus.id)
        menus_list = (await self.session.scalars(smtp)).all()

        return menus_list

    async def create_menu(self, title: str, desc: str) -> Menus:
        """
        Create new menu record in database

        :param title: title of menu
        :param desc: description of menu
        :return: created record in object view
        """
        menu = Menus(title=title, description=desc)

        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)

        return menu

    async def update_menu(self, menu_id: int, **kwargs) -> Menus | None:
        """
        Update menu

        :param menu_id: id of target menu
        :param kwargs: attributes of menu
        :return: updated model
        """
        menu = await self._get_menu(menu_id)

        for k, v in kwargs.items():
            if hasattr(menu, k):
                setattr(menu, k, v)

        await self.session.commit()
        await self.session.refresh(menu)

        return menu

    async def delete_menu(self, menu_id: int):
        """
        Delete menu record from database

        :param menu_id: if of target menu
        """
        menu = await self._get_menu(menu_id)

        await self.session.delete(menu)
        await self.session.commit()
