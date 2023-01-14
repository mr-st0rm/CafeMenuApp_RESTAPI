import typing

from app.database.models import Menus


def calculate_menu_submenus_and_dishes_list(menus: list) -> typing.List[Menus]:
    result_menu = list()

    for menu in menus:
        submenus_count = len(menu.sub_menus)
        dishes_count = sum([len(submenu.dishes) for submenu in menu.sub_menus])

        menu.submenus_count = submenus_count
        menu.dishes_count = dishes_count

        result_menu.append(menu)

    return result_menu


def calculate_menu_submenus_and_dishes(menu: Menus) -> Menus:
    submenus_count = len(menu.sub_menus)
    dishes_count = sum([len(submenu.dishes) for submenu in menu.sub_menus])

    menu.submenus_count = submenus_count
    menu.dishes_count = dishes_count

    return menu
