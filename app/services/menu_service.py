from fastapi import HTTPException

from app.database.models import Menus
from app.services import AbstractService, ServiceMixin


class MenuService(AbstractService, ServiceMixin):
    async def get_detail(self, menu_id: int) -> Menus:
        """
        Get menu object(db, cache) or raise error(404)

        :param menu_id: target menu id
        :return: menu object
        """
        cached_menu = await self.redis_cache.get_data(f"menu:{menu_id}")

        if cached_menu:
            return cached_menu

        menu = await self.main_repo.menu.menu_info(menu_id=menu_id)

        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        response_data = self.calculate_menu_submenus_and_dishes(menu)
        await self.redis_cache.save(f"menu:{menu_id}", response_data)

        return response_data

    async def get_list(self) -> list[Menus]:
        """
        Get list of menus(db, cache) and save to cache

        :return: list of menu objects
        """
        cached_menus = await self.redis_cache.get_data("menus")

        if cached_menus:
            # if list of menus cached
            return cached_menus

        menus = await self.main_repo.menu.get_all_menus()

        result_menu = list()

        for menu in menus:
            submenus_count = len(menu.sub_menus)
            dishes_count = sum(
                len(submenu.dishes) for submenu in menu.sub_menus
            )

            menu.submenus_count = submenus_count
            menu.dishes_count = dishes_count

            result_menu.append(menu)

        await self.redis_cache.save("menus", result_menu)

        return result_menu

    async def create(self, title: str, description: str) -> Menus:
        """
        Create new menu and clear menus list from cache

        :param title: menu title
        :param description: menu description
        :return: created menu object
        """
        menu = await self.main_repo.menu.create_menu(
            title=title, desc=description
        )

        menu_data = self.calculate_menu_submenus_and_dishes(menu)
        await self.redis_cache.clear("menus")

        return menu_data

    async def update(self, menu_id: int, **kwargs) -> Menus | None:
        """
        Update menu(db), clear target menu and menus list from cache

        :param menu_id: target menu id
        :param kwargs: attributes of menu
        :return: updated object of Menus
        """
        menu = await self.main_repo.menu.menu_info(menu_id=menu_id)

        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        updated_menu = await self.main_repo.menu.update_menu(menu_id, **kwargs)

        if updated_menu:
            updated_menu = self.calculate_menu_submenus_and_dishes(
                updated_menu
            )
            await self.redis_cache.save(
                f"menu:{updated_menu.id}", updated_menu
            )
            await self.redis_cache.clear("menus")

            return updated_menu

        return None

    async def delete(self, menu_id: int) -> bool:
        """
        Delete menu from db, clear target menu and menus list from cache

        :param menu_id: target menu id
        :return: bool
        """
        menu = await self.main_repo.menu.menu_info(menu_id=menu_id)

        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        await self.main_repo.menu.delete_menu(menu_id=menu_id)
        await self.redis_cache.clear(f"menu:{menu.id}", "menus")

        return True

    @staticmethod
    def calculate_menu_submenus_and_dishes(menu: Menus) -> Menus:
        """
        Calculate submenus and dishes count for menu

        :param menu: target menu
        :return: Menu modified object
        """
        submenus_count = len(menu.sub_menus)
        dishes_count = sum(len(submenu.dishes) for submenu in menu.sub_menus)

        menu.submenus_count = submenus_count
        menu.dishes_count = dishes_count

        return menu
