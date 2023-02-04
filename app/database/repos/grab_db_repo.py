from sqlalchemy import func, select
from sqlalchemy.engine import CursorResult

from app.database.models import Dishes, Menus, SubMenus
from app.database.repos import SQLAlchemyRepo


class GrabberDBRepo(SQLAlchemyRepo):
    async def grab_all_data(self) -> list:
        """
        Grab all data(menu, menu submenus and dishes of submenu) in one query

        :return: list of data
        """
        dishes = (
            select(
                func.array_agg(
                    func.json_build_object(
                        "title",
                        Dishes.title,
                        "description",
                        Dishes.description,
                        "price",
                        Dishes.price,
                    )
                )
            )
            .scalar_subquery()
            .where(Dishes.sub_menu_id == SubMenus.id)
        )

        submenu_dishes = func.array_agg(
            func.json_build_object(
                "title",
                SubMenus.title,
                "description",
                SubMenus.description,
                "dishes",
                dishes,
            )
        )

        db_data = (
            select(Menus.title, Menus.description, submenu_dishes)
            .join(Menus.sub_menus)
            .group_by(Menus.id)
            .order_by(Menus.id)
        )

        result: CursorResult = await self.session.execute(db_data)
        return result.all()
