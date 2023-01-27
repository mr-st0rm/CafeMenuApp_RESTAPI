from .dishes import Dishes
from .sub_menu import SubMenus
from .menu import Menus
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

# for updating MetaData in declarative_base
