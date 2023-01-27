from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.database.models import BaseModel


class Menus(BaseModel):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)

    title = Column(String)
    description = Column(String)

    sub_menus = relationship("SubMenus", backref="menu",
                             lazy="selectin", cascade="all, delete")

    created_date = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"{self.id} - {self.title}"
