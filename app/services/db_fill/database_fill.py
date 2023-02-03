import pydantic

from app.services import ServiceMixin
from app.services.db_fill.database_fill_models import Menu, Model


class DBFillerService(ServiceMixin):
    DEFAULT_PATH = "./data_for_db.json"
    """
    Test data structure
    "menu": {
        "description": "",
        "submenus" [
            "submenu": {
                "description": "",
                "dishes": [
                    "title": {
                        "description": "",
                        "price": ""
                    }
                ]
            }
        ]
    }

    """

    async def fill_db(self):
        menus: list[Menu] = self.read_db_data().__root__

        for menu in menus:
            created_menu = await self.main_repo.menu.create_menu(
                title=menu.title, desc=menu.description
            )

            for submenu in menu.submenus:
                created_submenu = await self.main_repo.submenu.create_submenu(
                    menu_id=created_menu.id,
                    title=submenu.title,
                    desc=submenu.description,
                )

                for dish in submenu.dishes:
                    await self.main_repo.dish.create_dish(
                        submenu_id=created_submenu.id,
                        title=dish.title,
                        desc=dish.description,
                        price=dish.price,
                    )

    def read_db_data(self) -> Model:
        menus = pydantic.parse_file_as(path=self.DEFAULT_PATH, type_=Model)

        return menus
