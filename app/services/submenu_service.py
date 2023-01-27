import typing

from fastapi import HTTPException

from app.database.models import SubMenus
from app.services import AbstractService, ServiceMixin


class SubmenuService(AbstractService, ServiceMixin):
    async def get_detail(self, submenu_id: int):
        submenu = await self.repo.submenu_info(submenu_id=submenu_id)

        if not submenu:
            raise HTTPException(status_code=404, detail="submenu not found")

        return self.calculate_count_dishes(submenu)

    async def get_list(self, menu_id: int):
        menu = await self.main_repo.menu.menu_info(menu_id=menu_id)

        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        return self.calculate_count_dishes_list(menu.sub_menus)

    async def create(self, menu_id: int, title: str, description: str):
        submenu = await self.repo.create_submenu(menu_id=menu_id, title=title, desc=description)

        return self.calculate_count_dishes(submenu)

    async def update(self, submenu_id: int, **kwargs):
        submenu = await self.repo.submenu_info(submenu_id=submenu_id)

        if not submenu:
            raise HTTPException(status_code=404, detail="menu not found")

        submenu = await self.repo.update_submenu(submenu_id, **kwargs)

        return self.calculate_count_dishes(submenu)

    async def delete(self, submenu_id: int):
        submenu = await self.repo.submenu_info(submenu_id=submenu_id)

        if not submenu:
            raise HTTPException(status_code=404, detail="submenu not found")

        await self.repo.delete_submenu(submenu_id=submenu_id)
        return True

    @staticmethod
    def calculate_count_dishes(submenu: SubMenus):
        dishes_count = len(submenu.dishes)

        submenu.dishes_count = dishes_count

        return submenu

    @staticmethod
    def calculate_count_dishes_list(submenus: typing.List[SubMenus]):
        result_list = list()

        for submenu in submenus:
            dishes_count = len(submenu.dishes)
            submenu.dishes_count = dishes_count

            result_list.append(submenu)

        return result_list
