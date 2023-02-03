from sqlalchemy import Numeric, func, select

from app.database.models import Dishes
from app.database.repos import SQLAlchemyRepo


class DishesRepo(SQLAlchemyRepo):
    async def _get_dish(self, dish_id: int) -> Dishes | None:
        """
        Get dish by PK from Dishes table

        :param dish_id: target dish id
        :return: Dish object or None
        """
        dish = await self.session.get(Dishes, dish_id)

        return dish

    async def dish_info(self, dish_id: int) -> Dishes | None:
        """
        Get Dish object by id

        :param dish_id: target dish id
        :return: Dish object or None
        """
        dish = await self._get_dish(dish_id)

        return dish

    async def get_all_dishes(self) -> list[Dishes]:
        """
        Get list of all dishes

        :return: list of Dishes objects
        """
        smtp = select(Dishes).order_by(Dishes.id)

        return (await self.session.scalars(smtp)).all()

    async def create_dish(
        self, submenu_id: int, title: str, desc: str, price: float
    ) -> Dishes:
        """
        Create new dish record in database

        :param submenu_id: id of target submenu for linking dish
        :param title: title of dish
        :param desc: description of dish
        :param price: price of dish (.2) float|int
        :return: created record in object view
        """
        dish = Dishes(
            sub_menu_id=submenu_id,
            title=title,
            description=desc,
            price=func.round(func.cast(price, Numeric), 2),
        )

        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)

        return dish

    async def update_dish(self, dish_id: int, **kwargs) -> Dishes | None:
        """
        Update dish

        :param dish_id: id of target dish
        :param kwargs: attributes of dish
        :return: updated model
        """
        dish = await self._get_dish(dish_id)

        for k, v in kwargs.items():
            if hasattr(dish, k):
                setattr(dish, k, v)

        await self.session.commit()
        await self.session.refresh(dish)

        return dish

    async def delete_dish(self, dish_id: int):
        """
        Delete dish record from database

        :param dish_id: target dish id
        """
        dish = await self._get_dish(dish_id)

        await self.session.delete(dish)
        await self.session.commit()
