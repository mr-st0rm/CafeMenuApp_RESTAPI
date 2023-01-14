import typing

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.database.repos.repo import Repo
from app.database.session_schema import repo_stub
from app.api.v1.schemas import request as req_model
from app.api.v1.schemas import response as res_model
from app.api.v1.utils import menu_utils

menu_router = APIRouter(prefix="/menus")


@menu_router.get("/", response_model=typing.List[res_model.Menu])
async def get_menus(repo: Repo = Depends(repo_stub)):
    all_menus = await repo.menu.get_all_menus()
    all_menus = menu_utils.calculate_menu_submenus_and_dishes_list(all_menus)

    return all_menus


@menu_router.post("/", response_model=res_model.Menu, status_code=201)
async def create_menu(menu: req_model.Menu, repo: Repo = Depends(repo_stub)):
    menu = await repo.menu.create_menu(menu.title, menu.description)
    menu = menu_utils.calculate_menu_submenus_and_dishes(menu)

    return menu


@menu_router.get("/{menu_id}", response_model=res_model.Menu)
async def get_menu_information(menu_id: int, repo: Repo = Depends(repo_stub)):
    menu = await repo.menu.menu_info(menu_id)

    if menu:
        menu = menu_utils.calculate_menu_submenus_and_dishes(menu)
        return menu

    raise HTTPException(status_code=404, detail="menu not found")


@menu_router.patch("/{menu_id}", response_model=res_model.Menu)
async def update_menu_information(menu_id: int, menu: req_model.Menu, repo: Repo = Depends(repo_stub)):
    menu = await repo.menu.update_menu(menu_id, menu.title, menu.description)

    if menu:
        menu = menu_utils.calculate_menu_submenus_and_dishes(menu)
        return menu

    raise HTTPException(status_code=404, detail="menu not found")


@menu_router.delete("/{menu_id}")
async def delete_menu(menu_id: int, repo: Repo = Depends(repo_stub)):
    menu = await repo.menu.delete_menu(menu_id)

    if menu:
        return JSONResponse(content={"status": menu, "message": "The menu has been deleted"})

    raise HTTPException(status_code=404, detail="menu not found")
