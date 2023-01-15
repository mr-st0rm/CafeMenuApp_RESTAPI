import typing

from sqlalchemy import select

from app.database.models import Dishes
from app.database.repos import SQLAlchemyRepo


class DishesRepo(SQLAlchemyRepo):
    async def _get_dish(self, dish_id: int) -> typing.Optional[Dishes]:
        dish = await self.session.get(Dishes, dish_id)

        return dish

    async def dish_info(self, dish_id: int) -> typing.Optional[Dishes]:
        dish = await self._get_dish(dish_id)

        return dish

    async def get_all_dishes(self) -> typing.List[Dishes]:
        smtp = select(Dishes).order_by(Dishes.id)

        return (await self.session.scalars(smtp)).all()

    async def create_dish(self, submenu_id: int, title: str, desc: str, price: float):
        dish = Dishes(sub_menu_id=submenu_id, title=title, description=desc, price=round(price, 2))

        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)

        return dish

    async def update_dish(self, dish_id: int, title: str = None, desc: str = None, price: float = 0):
        """ Not so good func, at now I dont know how make it more clear so"""
        dish = await self._get_dish(dish_id)

        if dish:
            if title:
                dish.title = title
            if desc:
                dish.description = desc

            if price:
                dish.price = round(price, 2)

            await self.session.commit()
            await self.session.refresh(dish)

            return dish

    async def delete_dish(self, dish_id: int):
        dish = await self._get_dish(dish_id)

        if dish:
            await self.session.delete(dish)
            await self.session.commit()

            return True
