from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database.models import BaseModel


class SubMenus(BaseModel):
    __tablename__ = "sub_menus"

    id = Column(Integer, primary_key=True)

    title = Column(String)
    description = Column(String)

    menu_id = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"))
    dishes = relationship("Dishes", backref="submenu",
                          lazy="selectin", cascade="all, delete")

    created_date = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"{self.id} - {self.title}"
