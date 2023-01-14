import typing

from sqlalchemy import select

from app.database.models import Menus
from app.database.repos import SQLAlchemyRepo


class MenuRepo(SQLAlchemyRepo):
    async def _get_menu(self, menu_id: int) -> typing.Optional[Menus]:
        menu = await self.session.get(Menus, menu_id)

        return menu

    async def menu_info(self, menu_id: int) -> typing.Optional[Menus]:
        menu = await self._get_menu(menu_id)

        return menu

    async def get_all_menus(self):
        smtp = select(Menus).order_by(Menus.id)
        menus_list = (await self.session.scalars(smtp)).all()

        return menus_list

    async def create_menu(self, title: str, desc: str) -> Menus:
        menu = Menus(title=title, description=desc)

        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)

        return menu

    async def update_menu(self, menu_id: int, title: str = None, desc: str = None):
        """ Not so good func, at now I dont know how make it more clear so"""
        menu = await self._get_menu(menu_id)

        if menu:
            if title:
                menu.title = title
            if desc:
                menu.description = desc

            await self.session.commit()
            await self.session.refresh(menu)

            return menu

    async def delete_menu(self, menu_id: int):
        menu = await self._get_menu(menu_id)

        if menu:
            await self.session.delete(menu)
            await self.session.commit()

            return True
