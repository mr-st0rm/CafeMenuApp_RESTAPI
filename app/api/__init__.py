from fastapi import FastAPI

from .events import event_handler
from .v1.routes.dish_routes import dish_router
from .v1.routes.menu_routes import menu_router
from .v1.routes.submenu_router import submenu_router


def register_api_routes(app: FastAPI):
    """
    Register all routes

    :param app: FastAPI obj
    :return: None
    """
    app.include_router(event_handler)
    app.include_router(menu_router, prefix="/api/v1")
    app.include_router(submenu_router, prefix="/api/v1")
    app.include_router(dish_router, prefix="/api/v1")
