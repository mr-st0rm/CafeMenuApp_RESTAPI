import typing

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.database.repos.repo import Repo
from app.database.session_schema import repo_stub
from app.api.v1.schemas import request as req_model
from app.api.v1.schemas import response as res_model

dish_router = APIRouter(prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes")


@dish_router.get("/", response_model=typing.List[res_model.Dish])
async def get_dishes(submenu_id: int, repo: Repo = Depends(repo_stub)):
    submenu = await repo.submenu.submenu_info(submenu_id)

    if submenu:
        return submenu.dishes

    raise HTTPException(status_code=404, detail="submenu not found")


@dish_router.get("/{dish_id}", response_model=res_model.Dish)
async def get_dish_information(dish_id: int, repo: Repo = Depends(repo_stub)):
    dish = await repo.dish.dish_info(dish_id)

    if dish:
        return dish

    raise HTTPException(status_code=404, detail="dish not found")


@dish_router.post("/", response_model=res_model.Dish, status_code=201)
async def create_dish(submenu_id: int, dish: req_model.Dish, repo: Repo = Depends(repo_stub)):
    dish = await repo.dish.create_dish(submenu_id, dish.title, dish.description, dish.price)

    if dish:
        return dish

    raise HTTPException(status_code=404, detail="submenu not found")


@dish_router.patch("/{dish_id}", response_model=res_model.Dish)
async def update_dish(dish_id: int, dish: req_model.Dish, repo: Repo = Depends(repo_stub)):
    dish = await repo.dish.update_dish(dish_id, dish.title, dish.description, dish.price)

    if dish:
        return dish

    raise HTTPException(status_code=404, detail="dish not found")


@dish_router.delete("/{dish_id}")
async def delete_dish(dish_id: int, repo: Repo = Depends(repo_stub)):
    dish = await repo.dish.delete_dish(dish_id)

    if dish:
        return JSONResponse(content={"status": dish, "message": "The dish has been deleted"})

    raise HTTPException(status_code=404, detail="dish not found")
