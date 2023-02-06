class MenuApiDocs:
    """Documentation descriptions for Menu urls"""

    GET_DETAIL = "Get detailed information about menu"
    GET_LIST = "Get list of menus"
    POST_CREATE = "Create new menu"
    PATCH_UPDATE = "Update an existing menu"
    DELETE = "Delete an existing menu, submenus and dishes linked to this menu"


class SubMenuApiDocs:
    """Documentation descriptions for SubMenu urls"""

    GET_DETAIL = "Get detailed information about submenu"
    GET_LIST = "Get list of submenus for an existing menu"
    POST_CREATE = "Create new submenu"
    PATCH_UPDATE = "Update an existing submenu"
    DELETE = "Delete an existing submenu and linked dishes"


class DishApiDocs:
    """Documentation descriptions for Dish urls"""

    GET_DETAIL = "Get detailed information about dish"
    GET_LIST = "Get list of all dishes"
    POST_CREATE = "Create new dish"
    PATCH_UPDATE = "Update an existing dish"
    DELETE = "Delete an existing dish"


class FillDatabaseDocs:
    POST_FILL = "Fill database with any records"


class ReportGenerators:
    POST_XLSX = "Create task in celery for generating .xlsx report"
    GET_XLSX = "Get detailed information about task"
    DOWNLOAD_XLSX = "Download generated .xlsx report"
