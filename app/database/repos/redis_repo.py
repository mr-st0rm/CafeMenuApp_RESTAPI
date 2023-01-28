import pickle
import typing

from aioredis import Redis


class RedisRepo:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save(self, key: str, value: typing.Any):
        value = pickle.dumps(value)
        await self.redis.set(key, value)

    async def get_data(self, key: str):
        data = await self.redis.get(key)

        if data:
            return pickle.loads(data)

    async def clear(self, *args):
        if args:
            await self.redis.delete(*args)
            return

        await self.redis.flushdb(asynchronous=True)
