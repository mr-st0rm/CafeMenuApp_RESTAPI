from typing import TypeAlias

from sqlalchemy.ext.declarative import declarative_base

BaseModel: TypeAlias = declarative_base()  # type: ignore

# for updating MetaData in declarative_base
from .dishes import Dishes
from .menu import Menus
from .sub_menu import SubMenus
