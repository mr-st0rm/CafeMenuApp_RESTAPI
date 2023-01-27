from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "title": "My title",
                "description": "My description"
            }
        }


class Dish(Menu):
    price: float

    class Config:
        schema_extra = {
            "example": {
                "title": "My title",
                "description": "My description",
                "price": 10.00
            }
        }
