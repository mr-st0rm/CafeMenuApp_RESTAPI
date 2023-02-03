from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)

from app.database.models import BaseModel


class Dishes(BaseModel):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)

    title = Column(String)
    description = Column(String)
    price = Column(Numeric(scale=2), nullable=False)

    sub_menu_id = Column(
        Integer, ForeignKey("sub_menus.id", ondelete="CASCADE")
    )

    created_date = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"{self.id} - {self.title}"
