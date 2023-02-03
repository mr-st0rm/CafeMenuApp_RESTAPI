import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database.models import BaseModel


class Menus(BaseModel):
    __tablename__ = "menus"

    id = sa.Column(sa.Integer, primary_key=True)

    title = sa.Column(sa.String)
    description = sa.Column(sa.String)

    sub_menus = relationship(
        "SubMenus", backref="menu", lazy="selectin", cascade="all, delete"
    )

    created_date = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())

    def __repr__(self):
        return f"{self.id} - {self.title}"
