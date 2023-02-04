import typing

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repos.repo import (
    DishesRepo,
    GrabberDBRepo,
    MenuRepo,
    Repo,
    SubMenuRepo,
)


def repo_stub():
    """Yes, really"""
    raise NotImplementedError


class DBProvider:
    def __init__(self, pool):
        self.pool = pool

    async def get_repo(self) -> typing.AsyncGenerator:
        """
        Generator for Repo class object

        :return: repo object
        """
        session: AsyncSession = self.pool()

        try:
            repo = Repo(
                session, MenuRepo, SubMenuRepo, DishesRepo, GrabberDBRepo
            )
            yield repo
        finally:
            await session.close()
