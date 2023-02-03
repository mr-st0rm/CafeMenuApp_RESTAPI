from sqlalchemy import select

from app.database.models import SubMenus
from app.database.repos import SQLAlchemyRepo


class SubMenuRepo(SQLAlchemyRepo):
    async def _get_submenu(self, submenu_id: int) -> SubMenus | None:
        """
         Get submenu by PK from SubMenus table

        :param submenu_id: target id of submenu
        :return: Submenus object or None
        """
        submenu = await self.session.get(SubMenus, submenu_id)

        return submenu

    async def get_all_submenus_for_menu(self, menu_id: int) -> list[SubMenus]:
        """
        Get list of all submenus for target menu

        :param menu_id: target menu id
        :return: list of SubMenus objects
        """
        smtp = (
            select(SubMenus)
            .where(SubMenus.menu_id == menu_id)
            .order_by(SubMenus.id)
        )
        submenus = await self.session.scalars(smtp)

        return submenus.all()

    async def submenu_info(self, submenu_id: int) -> SubMenus | None:
        """
        Get SubMenu object by id

        :param submenu_id: target submenu id
        :return: Submenus object or None
        """
        submenu = await self._get_submenu(submenu_id)

        return submenu

    async def create_submenu(
        self, menu_id: int, title: str, desc: str
    ) -> SubMenus:
        """
        Create new submenu record in database

        :param menu_id: if of target menu for linking dish
        :param title: title of submenu
        :param desc: description of submenu
        :return: created record in object view
        """
        submenu = SubMenus(menu_id=menu_id, title=title, description=desc)

        self.session.add(submenu)
        await self.session.commit()
        await self.session.refresh(submenu)

        return submenu

    async def update_submenu(
        self, submenu_id: int, **kwargs
    ) -> SubMenus | None:
        """
        Update target submenu

        :param submenu_id: target submenu id
        :param kwargs: submenu attributes
        :return: optional updated Submenu
        """
        submenu = await self._get_submenu(submenu_id)

        for k, v in kwargs.items():
            if hasattr(submenu, k):
                setattr(submenu, k, v)

        await self.session.commit()
        await self.session.refresh(submenu)

        return submenu

    async def delete_submenu(self, submenu_id: int):
        """
        Delete submenu with linked dishes

        :param submenu_id: target submenu id
        """
        submenu = await self._get_submenu(submenu_id)

        await self.session.delete(submenu)
        await self.session.commit()
