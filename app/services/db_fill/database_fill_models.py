from pydantic import BaseModel


class Dish(BaseModel):
    title: str
    description: str
    price: float


class Submenu(BaseModel):
    title: str
    description: str
    dishes: list[Dish]


class Menu(BaseModel):
    title: str
    description: str
    submenus: list[Submenu]


class Model(BaseModel):
    __root__: list[Menu]
