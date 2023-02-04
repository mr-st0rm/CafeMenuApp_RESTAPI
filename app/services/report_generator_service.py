from app.services import ServiceMixin
from app.services.db_fill.database_fill_models import Menu


class XLSXReportGenerator(ServiceMixin):
    async def get_all_data(self) -> list[dict]:
        """
        Grab all data from database and return list of parsed Menu objects dict

        :return: Menu objects list
        """
        data: list = await self.main_repo.grabber.grab_all_data()
        menus_list: list[Menu] = self._parse_menu(data)

        menus_dict = [menu.dict() for menu in menus_list]

        return menus_dict

    @staticmethod
    def _parse_menu(menu_data: list) -> list[Menu]:
        """
        Parse Menu objects from db result list

        :param menu_data: db menus list
        :return: Menu objects list
        """
        menus = list()

        for menu in menu_data:
            title, description, submenus = menu

            parsed_menu = Menu(
                title=title, description=description, submenus=submenus
            )
            menus.append(parsed_menu)

        return menus
