import typing

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.database.repos.repo import Repo
from app.database.session_schema import repo_stub
from app.api.v1.schemas import request as req_model
from app.api.v1.schemas import response as res_model
from app.api.v1.utils import submenu_utils

submenu_router = APIRouter(prefix="/menus/{menu_id}/submenus")


@submenu_router.get("/", response_model=typing.List[res_model.SubMenu])
async def get_all_submenus(menu_id: int, repo: Repo = Depends(repo_stub)):
    menu = await repo.menu.menu_info(menu_id)

    if menu:
        submenus = submenu_utils.calculate_submenu_dishes_list(menu.sub_menus)
        return submenus

    raise HTTPException(status_code=404, detail="menu not found")


@submenu_router.get("/{submenu_id}", response_model=res_model.SubMenu)
async def get_submenu_information(submenu_id: int, repo: Repo = Depends(repo_stub)):
    submenu = await repo.submenu.submenu_info(submenu_id)

    if submenu:
        submenu = submenu_utils.calculate_submenu_dishes(submenu)
        return submenu

    raise HTTPException(status_code=404, detail="submenu not found")


@submenu_router.post("/", response_model=res_model.SubMenu, status_code=201)
async def create_submenu(menu_id: int, submenu: req_model.Menu, repo: Repo = Depends(repo_stub)):
    submenu = await repo.submenu.create_submenu(menu_id, submenu.title, submenu.description)
    submenu = submenu_utils.calculate_submenu_dishes(submenu)

    return submenu


@submenu_router.patch("/{submenu_id}", response_model=res_model.SubMenu)
async def update_submenu_information(submenu_id: int, submenu: req_model.Menu, repo: Repo = Depends(repo_stub)):
    submenu = await repo.submenu.update_submenu(submenu_id, submenu.title, submenu.description)

    if submenu:
        submenu = submenu_utils.calculate_submenu_dishes(submenu)
        return submenu

    raise HTTPException(status_code=404, detail="submenu not found")


@submenu_router.delete("/{submenu_id}")
async def delete_submenu(submenu_id: int, repo: Repo = Depends(repo_stub)):
    menu = await repo.submenu.delete_submenu(submenu_id)

    if menu:
        return JSONResponse(content={"status": menu, "message": "The submenu has been deleted"})

    raise HTTPException(status_code=404, detail="menu not found")
