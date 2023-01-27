from pydantic import BaseModel


class OrmModeOn(BaseModel):
    class Config:
        orm_mode = True


class BaseMenu(OrmModeOn):
    id: str
    title: str
    description: str


class Menu(BaseMenu):
    submenus_count: int
    dishes_count: int


class SubMenu(BaseMenu):
    dishes_count: int


class Dish(BaseMenu):
    price: str
