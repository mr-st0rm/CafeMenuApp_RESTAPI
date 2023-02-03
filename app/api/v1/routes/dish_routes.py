from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api.v1.docs.menu_methods_description import DishApiDocs
from app.api.v1.schemas import request as req_model
from app.api.v1.schemas import response as res_model
from app.services.service import Services, service_stub

dish_router = APIRouter(prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes")


@dish_router.get(
    "/",
    tags=["Dish"],
    description=DishApiDocs.GET_LIST,
    summary=DishApiDocs.GET_LIST,
    response_model=list[res_model.Dish],
)
async def get_dishes(
    services: Services = Depends(service_stub),
) -> list[res_model.Dish]:
    """
    Get list of all dishes

    :param services: Services for business logic
    :return: list of Dish
    """
    dishes = await services.dishes_service.get_list()

    return dishes


@dish_router.get(
    "/{dish_id}",
    tags=["Dish"],
    description=DishApiDocs.GET_DETAIL,
    summary=DishApiDocs.GET_DETAIL,
    response_model=res_model.Dish,
)
async def get_dish_information(
    dish_id: int, services: Services = Depends(service_stub)
) -> res_model.Dish:
    """
    Get detailed info about dish

    :param dish_id: id of target dish
    :param services: Services for business logic
    :return: target Dish or not found
    """
    dish = await services.dishes_service.get_detail(dish_id=dish_id)

    return dish


@dish_router.post(
    "/",
    tags=["Dish"],
    description=DishApiDocs.POST_CREATE,
    summary=DishApiDocs.POST_CREATE,
    response_model=res_model.Dish,
    status_code=status.HTTP_201_CREATED,
)
async def create_dish(
    submenu_id: int,
    dish: req_model.Dish,
    services: Services = Depends(service_stub),
):
    """
    Create new dish for target SubMenu

    :param submenu_id: submenu id
    :param dish: parsed Dish model from request
    :param services: Services for business logic
    :return: model of created Dish
    """
    dish = await services.dishes_service.create(
        submenu_id, dish.title, dish.description, dish.price
    )

    return dish


@dish_router.patch(
    "/{dish_id}",
    tags=["Dish"],
    description=DishApiDocs.PATCH_UPDATE,
    summary=DishApiDocs.PATCH_UPDATE,
    response_model=res_model.Dish,
)
async def update_dish(
    dish_id: int,
    dish: req_model.Dish,
    services: Services = Depends(service_stub),
) -> res_model.Dish | None:
    """
    Update an exists dish

    :param dish_id: id of target dish
    :param dish: parser Dish model from request
    :param services: Services for business logic
    :return: updated Dish model
    """
    updated_dish = await services.dishes_service.update(
        dish_id,
        title=dish.title,
        description=dish.description,
        price=dish.price,
    )

    return updated_dish


@dish_router.delete(
    "/{dish_id}",
    tags=["Dish"],
    description=DishApiDocs.DELETE,
    summary=DishApiDocs.DELETE,
)
async def delete_dish(
    dish_id: int, services: Services = Depends(service_stub)
):
    """
    Delete dish

    :param dish_id: id of target dish
    :param services: Services for business logic
    :return: json response with message field
    """
    dish = await services.dishes_service.delete(dish_id)

    return JSONResponse(
        content={"status": dish, "message": "The dish has been deleted"}
    )
