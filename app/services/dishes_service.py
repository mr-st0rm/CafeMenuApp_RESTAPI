from fastapi import HTTPException

from app.database.models import Dishes
from app.services import AbstractService, ServiceMixin


class DishesService(AbstractService, ServiceMixin):
    async def get_detail(self, dish_id: int) -> Dishes:
        """
        Get dish object(db, cache) or raise error(404)

        :param dish_id: target dish id
        :return: dish object
        """
        cached_dish = await self.redis_cache.get_data(f"dish:{dish_id}")

        if cached_dish:
            return cached_dish

        dish = await self.main_repo.dish.dish_info(dish_id)

        if not dish:
            raise HTTPException(status_code=404, detail="dish not found")

        await self.redis_cache.save(f"dish:{dish_id}", dish)

        return dish

    async def get_list(self) -> list[Dishes]:
        """
        Get list of dishes(db, cache) and save to cache

        :return: list of dish objects
        """
        cached_dishes = await self.redis_cache.get_data("dishes")

        if cached_dishes:
            return cached_dishes

        dishes = await self.main_repo.dish.get_all_dishes()
        await self.redis_cache.save("dishes", dishes)

        return dishes

    async def create(
        self, submenu_id: int, title: str, description: str, price: float
    ) -> Dishes:
        """
        Create new dish and clear cache

        :param submenu_id: target submenu id for linking
        :param title: dish title
        :param description: dish description
        :param price: float
        :return: created dish object
        """
        submenu = await self.main_repo.submenu.submenu_info(
            submenu_id=submenu_id
        )

        if not submenu:
            raise HTTPException(status_code=404, detail="submenu not found")

        dish = await self.main_repo.dish.create_dish(
            submenu_id=submenu_id, title=title, desc=description, price=price
        )
        await self.redis_cache.clear()

        return dish

    async def update(self, dish_id: int, **kwargs) -> Dishes | None:
        """
        Update dish(db) and clear dishes list from cache

        :param dish_id: target dish id
        :param kwargs: attributes of dish
        :return: updated object of Dish
        """
        dish = await self.main_repo.dish.dish_info(dish_id)

        if not dish:
            raise HTTPException(status_code=404, detail="dish not found")

        price = kwargs.get("price")

        if price:
            kwargs["price"] = round(price, 2)

        updated_dish = await self.main_repo.dish.update_dish(dish_id, **kwargs)

        if updated_dish:
            await self.redis_cache.save(
                f"dish:{updated_dish.id}", updated_dish
            )
            await self.redis_cache.clear("dishes")

            return updated_dish

        return None

    async def delete(self, dish_id: int) -> bool:
        """
        Delete dish from db and clear cache

        :param dish_id: target dish id
        :return: bool
        """
        dish = await self.main_repo.dish.dish_info(dish_id=dish_id)

        if not dish:
            raise HTTPException(status_code=404, detail="dish not found")

        await self.main_repo.dish.delete_dish(dish_id)
        await self.redis_cache.clear()

        return True
