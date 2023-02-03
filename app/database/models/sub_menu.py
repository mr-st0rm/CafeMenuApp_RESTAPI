import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database.models import BaseModel


class SubMenus(BaseModel):  # type: ignore
    __tablename__ = "sub_menus"

    id = sa.Column(sa.Integer, primary_key=True)

    title = sa.Column(sa.String)
    description = sa.Column(sa.String)

    menu_id = sa.Column(
        sa.Integer, sa.ForeignKey("menus.id", ondelete="CASCADE")
    )
    dishes = relationship(
        "Dishes", backref="submenu", lazy="selectin", cascade="all, delete"
    )

    created_date = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())

    def __repr__(self):
        return f"{self.id} - {self.title}"
