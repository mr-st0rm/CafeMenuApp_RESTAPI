from fastapi import HTTPException

from app.database.models import Menus
from app.services import AbstractService, ServiceMixin


class MenuService(AbstractService, ServiceMixin):
    async def get_detail(self, menu_id: int):
        menu = await self.repo.menu_info(menu_id=menu_id)

        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        return self.calculate_menu_submenus_and_dishes(menu)

    async def get_list(self):
        menus = await self.repo.get_all_menus()

        result_menu = list()

        for menu in menus:
            submenus_count = len(menu.sub_menus)
            dishes_count = sum(len(submenu.dishes)
                               for submenu in menu.sub_menus)

            menu.submenus_count = submenus_count
            menu.dishes_count = dishes_count

            result_menu.append(menu)

        return result_menu

    async def create(self, title: str, description: str):
        menu = await self.repo.create_menu(title=title, desc=description)

        return self.calculate_menu_submenus_and_dishes(menu)

    async def update(self, menu_id: int, **kwargs):
        menu = await self.repo.menu_info(menu_id=menu_id)

        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        menu = await self.repo.update_menu(menu_id, **kwargs)

        return self.calculate_menu_submenus_and_dishes(menu)

    async def delete(self, menu_id: int):
        menu = await self.repo.menu_info(menu_id=menu_id)

        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        await self.repo.delete_menu(menu_id=menu_id)
        return True

    @staticmethod
    def calculate_menu_submenus_and_dishes(menu: Menus):
        submenus_count = len(menu.sub_menus)
        dishes_count = sum(len(submenu.dishes) for submenu in menu.sub_menus)

        menu.submenus_count = submenus_count
        menu.dishes_count = dishes_count

        return menu
