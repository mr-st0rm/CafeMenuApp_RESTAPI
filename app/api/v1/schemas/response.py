from pydantic import BaseModel


class OrmModeOn(BaseModel):
    class Config:
        orm_mode = True


class BaseMenu(OrmModeOn):
    """Base response model for orm-models"""

    id: str
    title: str
    description: str


class Menu(BaseMenu):
    """Response model of Menu"""

    submenus_count: int
    dishes_count: int


class SubMenu(BaseMenu):
    """Response model of SubMenu"""

    dishes_count: int


class Dish(BaseMenu):
    """Response model of Dish"""

    price: str


class CreatedTask(BaseModel):
    task_id: str


class DetailedTask(CreatedTask):
    status: str
    result: str | None
