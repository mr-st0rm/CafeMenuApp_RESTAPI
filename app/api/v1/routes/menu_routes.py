import typing

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.v1.schemas import request as req_model
from app.api.v1.schemas import response as res_model
from app.services.service import service_stub, Services
from app.api.v1.docs.menu_methods_description import MenuApiDocs

menu_router = APIRouter(prefix="/menus")


@menu_router.get(
    "/",
    tags=["Menu"], description=MenuApiDocs.GET_LIST, summary=MenuApiDocs.GET_LIST,
    response_model=typing.List[res_model.Menu]
)
async def get_menus(services: Services = Depends(service_stub)):
    all_menus = await services.menu_service.get_list()

    return all_menus


@menu_router.post(
    "/",
    tags=["Menu"], description=MenuApiDocs.POST_CREATE, summary=MenuApiDocs.POST_CREATE,
    response_model=res_model.Menu, status_code=201
)
async def create_menu(menu: req_model.Menu, services: Services = Depends(service_stub)):
    menu = await services.menu_service.create(title=menu.title, description=menu.description)

    return menu


@menu_router.get(
    "/{menu_id}",
    tags=["Menu"], description=MenuApiDocs.GET_DETAIL, summary=MenuApiDocs.GET_DETAIL,
    response_model=res_model.Menu
)
async def get_menu_information(menu_id: int, services: Services = Depends(service_stub)):
    menu = await services.menu_service.get_detail(menu_id=menu_id)

    return menu


@menu_router.patch(
    "/{menu_id}",
    tags=["Menu"], description=MenuApiDocs.PATCH_UPDATE, summary=MenuApiDocs.PATCH_UPDATE,
    response_model=res_model.Menu
)
async def update_menu_information(menu_id: int, menu: req_model.Menu, services: Services = Depends(service_stub)):
    menu = await services.menu_service.update(menu_id, title=menu.title, description=menu.description)

    return menu


@menu_router.delete("/{menu_id}", tags=["Menu"], description=MenuApiDocs.DELETE, summary=MenuApiDocs.DELETE)
async def delete_menu(menu_id: int, services: Services = Depends(service_stub)):
    menu = await services.menu_service.delete(menu_id)

    return JSONResponse(content={"status": menu, "message": "The menu has been deleted"})

