from pydantic import BaseModel


class Menu(BaseModel):
    """Request schema of Menu(Submenu) model"""

    title: str
    description: str

    class Config:
        schema_extra = {
            "example": {"title": "My title", "description": "My description"}
        }


class Dish(Menu):
    """Request schema of Dish model"""

    price: float

    class Config:
        schema_extra = {
            "example": {
                "title": "My title",
                "description": "My description",
                "price": 10.00,
            }
        }
