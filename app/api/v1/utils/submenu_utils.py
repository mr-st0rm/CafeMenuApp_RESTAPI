import typing

from app.database.models import SubMenus


def calculate_submenu_dishes_list(submenus: list) -> typing.List[SubMenus]:
    result_submenu = list()

    for submenu in submenus:
        dishes_count = len(submenu.dishes)

        submenu.dishes_count = dishes_count

        result_submenu.append(submenu)

    return result_submenu


def calculate_submenu_dishes(submenu: SubMenus) -> SubMenus:
    submenu.dishes_count = len(submenu.dishes)

    return submenu
