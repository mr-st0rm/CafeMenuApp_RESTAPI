from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str


class Dish(Menu):
    price: float
