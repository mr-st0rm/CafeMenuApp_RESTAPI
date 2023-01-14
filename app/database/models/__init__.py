from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

# for updating MetaData in declarative_base
from .menu import Menus
from .sub_menu import SubMenus
from .dishes import Dishes
