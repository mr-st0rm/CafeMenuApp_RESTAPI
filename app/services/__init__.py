from abc import ABC, abstractmethod


from app.database.repos.repo import (
    RedisRepo,
    Repo,
)


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
    def __init__(
        self,
        main_repo: Repo,
        redis: RedisRepo,
    ):
        self.main_repo: Repo = main_repo
        self.redis_cache: RedisRepo = redis
