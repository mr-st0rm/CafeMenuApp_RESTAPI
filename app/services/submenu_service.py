from fastapi import HTTPException

from app.database.models import SubMenus
from app.services import AbstractService, ServiceMixin


class SubmenuService(AbstractService, ServiceMixin):
    async def get_detail(self, submenu_id: int) -> SubMenus | None:
        """
        Get submenu object(db, cache) or raise error(404)

        :param submenu_id: target submenu id
        :return: submenu object
        """
        cached_submenu = await self.redis_cache.get_data(
            f"submenu:{submenu_id}"
        )

        if cached_submenu:
            return cached_submenu

        submenu = await self.main_repo.submenu.submenu_info(
            submenu_id=submenu_id
        )

        if not submenu:
            raise HTTPException(status_code=404, detail="submenu not found")

        response_data = self.calculate_count_dishes(submenu)
        await self.redis_cache.save(f"submenu:{submenu_id}", response_data)

        return response_data

    async def get_list(self, menu_id: int) -> list[SubMenus]:
        """
        Get list of submenus(db, cache) and save to cache

        :param menu_id: target menu id where submenus linked
        :return: list of submenu objects
        """
        cached_submenus = await self.redis_cache.get_data(
            f"submenus:{menu_id}"
        )

        if cached_submenus:
            return cached_submenus

        menu = await self.main_repo.menu.menu_info(menu_id=menu_id)

        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        submenus = self.calculate_count_dishes_list(menu.sub_menus)
        await self.redis_cache.save(f"submenus:{menu_id}", submenus)

        return submenus

    async def create(
        self, menu_id: int, title: str, description: str
    ) -> SubMenus:
        """


        :param menu_id:
        :param title:
        :param description:
        :return:
        """
        submenu = await self.main_repo.submenu.create_submenu(
            menu_id=menu_id, title=title, desc=description
        )

        await self.redis_cache.clear()

        return self.calculate_count_dishes(submenu)

    async def update(self, submenu_id: int, **kwargs) -> SubMenus | None:
        """
        Update submenu(db) and clear submenus list from cache

        :param submenu_id: target submenu id
        :param kwargs: attributes of submenu
        :return: updated object of SubMenus
        """
        submenu = await self.main_repo.submenu.submenu_info(
            submenu_id=submenu_id
        )

        if not submenu:
            raise HTTPException(status_code=404, detail="menu not found")

        updated_submenu = await self.main_repo.submenu.update_submenu(
            submenu_id, **kwargs
        )

        if updated_submenu:
            updated_submenu = self.calculate_count_dishes(updated_submenu)
            await self.redis_cache.save(
                f"submenu:{updated_submenu.id}", updated_submenu
            )
            await self.redis_cache.clear(f"submenus:{updated_submenu.menu_id}")

            return updated_submenu

        return None

    async def delete(self, submenu_id: int) -> bool:
        """
        Delete submenu from db and clear cache

        :param submenu_id: target submenu id
        :return: bool
        """
        submenu = await self.main_repo.submenu.submenu_info(
            submenu_id=submenu_id
        )

        if not submenu:
            raise HTTPException(status_code=404, detail="submenu not found")

        await self.main_repo.submenu.delete_submenu(submenu_id=submenu_id)
        await self.redis_cache.clear()

        return True

    @staticmethod
    def calculate_count_dishes(submenu: SubMenus) -> SubMenus:
        """
        Calculate dishes count for submenu

        :param submenu: submenu object
        :return: SubMenus modified object
        """
        dishes_count = len(submenu.dishes)

        submenu.dishes_count = dishes_count

        return submenu

    @staticmethod
    def calculate_count_dishes_list(
        submenus: list[SubMenus],
    ) -> list[SubMenus]:
        """
        Calculate dishes count for submenus

        :param submenus: submenu objects list
        :return: SubMenus modified objects list
        """
        result_list = list()

        for submenu in submenus:
            dishes_count = len(submenu.dishes)
            submenu.dishes_count = dishes_count

            result_list.append(submenu)

        return result_list
