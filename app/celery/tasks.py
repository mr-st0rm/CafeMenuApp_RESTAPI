import uuid

import xlsxwriter

from app.services.db_fill.database_fill_models import Menu

from .celery_app import celery


@celery.task(name="app.create_report_xlsx:celery")
def create_report_xlsx(menus_list: list[dict]):
    name = f"{uuid.uuid4().hex}.xlsx"
    generate_xlsx(f"reports/{name}", menus_list)

    return name


def generate_xlsx(name: str, menus: list[dict]):
    """
    Generate xlsx file for menu

    :param name: filename
    :param menus: list of menus
    """
    with xlsxwriter.Workbook(name) as book:
        book_sheet = book.add_worksheet("Menu")
        column = 0
        row = 0

        for i, menu in enumerate(menus):
            menu = Menu(**menu)

            book_sheet.write(row, column, menu.title)
            book_sheet.write(row, column + 1, menu.description)

            column += 2
            row += 1

            for submenu in menu.submenus:
                book_sheet.write(row, column, submenu.title)
                book_sheet.write(row, column + 1, submenu.description)

                row += 1
                column += 2

                for dish in submenu.dishes:
                    book_sheet.write(row, column, dish.title)
                    book_sheet.write(row, column + 1, dish.description)
                    book_sheet.write(row, column + 2, dish.price)

                    row += 1

                column -= 2

            column = 0
            row += 2
