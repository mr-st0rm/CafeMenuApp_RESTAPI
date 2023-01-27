from abc import ABC, abstractmethod
from typing import Union, Optional

from app.database.repos.repo import MenuRepo, SubMenuRepo, DishesRepo, Repo


class AbstractService(ABC):
    @abstractmethod
    async def get_detail(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def get_list(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplemented


class ServiceMixin:
    def __init__(self, repo: Union[MenuRepo, SubMenuRepo, DishesRepo], main_repo: Optional[Repo] = None):
        self.repo = repo
        self.main_repo = main_repo
