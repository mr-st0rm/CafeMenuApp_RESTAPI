from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepo:
    """Base Repo class with async_session argument"""

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
