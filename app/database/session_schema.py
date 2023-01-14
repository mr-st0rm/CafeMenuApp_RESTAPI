import abc
import typing

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repos.repo import Repo, MenuRepo, SubMenuRepo, DishesRepo


def repo_stub():
    """ Yes, really """
    raise NotImplemented


class DBProvider:
    def __init__(self, pool):
        self.pool = pool

    async def get_repo(self) -> typing.Generator:
        session: AsyncSession = self.pool()

        try:
            repo = Repo(session, MenuRepo, SubMenuRepo, DishesRepo)
            yield repo
        finally:
            await session.close()
