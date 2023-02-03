import pickle
import typing

from aioredis import Redis


class RedisRepo:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save(self, key: str, value: typing.Any):
        """
        Set pickled value to key in redis db

        :param key: string
        :param value: any data
        """
        value = pickle.dumps(value)
        await self.redis.set(key, value)

    async def get_data(self, key: str) -> typing.Any | None:
        """
        Get data by key from redis db

        :param key: string
        :return: data or None
        """
        data = await self.redis.get(key)

        if data:
            return pickle.loads(data)

        return None

    async def clear(self, *args):
        """
        Clear redis db by keys or flush db

        :param args: keys(strings)
        """
        if args:
            await self.redis.delete(*args)
            return

        await self.redis.flushdb(asynchronous=True)
