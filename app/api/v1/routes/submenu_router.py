from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.v1.docs.menu_methods_description import SubMenuApiDocs
from app.api.v1.schemas import request as req_model
from app.api.v1.schemas import response as res_model
from app.services.service import Services, service_stub

submenu_router = APIRouter(prefix="/menus/{menu_id}/submenus")


@submenu_router.get(
    "/",
    tags=["Submenu"], description=SubMenuApiDocs.GET_LIST, summary=SubMenuApiDocs.GET_LIST,
    response_model=list[res_model.SubMenu]
)
async def get_all_submenus(menu_id: int, services: Services = Depends(service_stub)):
    submenus = await services.submenu_service.get_list(menu_id=menu_id)

    return submenus


@submenu_router.get(
    "/{submenu_id}",
    tags=["Submenu"], description=SubMenuApiDocs.GET_DETAIL, summary=SubMenuApiDocs.GET_DETAIL,
    response_model=res_model.SubMenu
)
async def get_submenu_information(submenu_id: int, services: Services = Depends(service_stub)):
    submenu = await services.submenu_service.get_detail(submenu_id=submenu_id)

    return submenu


@submenu_router.post(
    "/",
    tags=["Submenu"], description=SubMenuApiDocs.POST_CREATE, summary=SubMenuApiDocs.POST_CREATE,
    response_model=res_model.SubMenu, status_code=201
)
async def create_submenu(menu_id: int, submenu: req_model.Menu, services: Services = Depends(service_stub)):
    submenu = await services.submenu_service.create(
        menu_id=menu_id,
        title=submenu.title,
        description=submenu.description
    )

    return submenu


@submenu_router.patch(
    "/{submenu_id}",
    tags=["Submenu"], description=SubMenuApiDocs.PATCH_UPDATE, summary=SubMenuApiDocs.PATCH_UPDATE,
    response_model=res_model.SubMenu
)
async def update_submenu_information(
        submenu_id: int,
        submenu: req_model.Menu, services: Services = Depends(service_stub)
):
    submenu = await services.submenu_service.update(submenu_id, title=submenu.title, description=submenu.description)

    return submenu


@submenu_router.delete(
    "/{submenu_id}",
    tags=["Submenu"], description=SubMenuApiDocs.DELETE, summary=SubMenuApiDocs.DELETE
)
async def delete_submenu(submenu_id: int, services: Services = Depends(service_stub)):
    menu = await services.submenu_service.delete(submenu_id=submenu_id)

    return JSONResponse(content={"status": menu, "message": "The submenu has been deleted"})
