import typing

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.v1.schemas import request as req_model
from app.api.v1.schemas import response as res_model
from app.services.service import service_stub, Services

dish_router = APIRouter(prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes")


@dish_router.get("/", response_model=typing.List[res_model.Dish])
async def get_dishes(services: Services = Depends(service_stub)):
    dishes = await services.dishes_service.get_list()

    return dishes


@dish_router.get("/{dish_id}", response_model=res_model.Dish)
async def get_dish_information(dish_id: int, services: Services = Depends(service_stub)):
    dish = await services.dishes_service.get_detail(dish_id=dish_id)

    return dish


@dish_router.post("/", response_model=res_model.Dish, status_code=201)
async def create_dish(submenu_id: int, dish: req_model.Dish, services: Services = Depends(service_stub)):
    dish = await services.dishes_service.create(submenu_id, dish.title, dish.description, dish.price)

    return dish


@dish_router.patch("/{dish_id}", response_model=res_model.Dish)
async def update_dish(dish_id: int, dish: req_model.Dish, services: Services = Depends(service_stub)):
    dish = await services.dishes_service.update(
        dish_id, title=dish.title, description=dish.description, price=dish.price
    )

    return dish


@dish_router.delete("/{dish_id}")
async def delete_dish(dish_id: int, services: Services = Depends(service_stub)):
    dish = await services.dishes_service.delete(dish_id)

    return JSONResponse(content={"status": dish, "message": "The dish has been deleted"})
