import sqlalchemy as sa

from app.database.models import BaseModel


class Dishes(BaseModel):
    __tablename__ = "dishes"

    id = sa.Column(sa.Integer, primary_key=True)

    title = sa.Column(sa.String)
    description = sa.Column(sa.String)
    price = sa.Column(sa.Numeric(scale=2), nullable=False)

    sub_menu_id = sa.Column(
        sa.Integer, sa.ForeignKey("sub_menus.id", ondelete="CASCADE")
    )

    created_date = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())

    def __repr__(self):
        return f"{self.id} - {self.title}"
