import typing

from sqlalchemy import select

from app.database.models import SubMenus
from app.database.repos import SQLAlchemyRepo


class SubMenuRepo(SQLAlchemyRepo):
    async def _get_submenu(self, submenu_id: int) -> typing.Optional[SubMenus]:
        submenu = await self.session.get(SubMenus, submenu_id)

        return submenu

    async def get_all_submenus_for_menu(self, menu_id: int) -> typing.List[SubMenus]:
        smtp = select(SubMenus).where(SubMenus.menu_id == menu_id).order_by(SubMenus.id)
        submenus = await self.session.scalars(smtp)

        return submenus.all()

    async def submenu_info(self, submenu_id: int) -> typing.Optional[SubMenus]:
        submenu = await self._get_submenu(submenu_id)

        return submenu

    async def create_submenu(self, menu_id: int, title: str, desc: str) -> SubMenus:
        submenu = SubMenus(menu_id=menu_id, title=title, description=desc)

        self.session.add(submenu)
        await self.session.commit()
        await self.session.refresh(submenu)

        return submenu

    async def update_submenu(self, submenu_id: int, **kwargs):
        submenu = await self._get_submenu(submenu_id)

        for k, v in kwargs.items():
            if hasattr(submenu, k):
                setattr(submenu, k, v)

        await self.session.commit()
        await self.session.refresh(submenu)

        return submenu

    async def delete_submenu(self, submenu_id: int):
        submenu = await self._get_submenu(submenu_id)

        await self.session.delete(submenu)
        await self.session.commit()

        return True
