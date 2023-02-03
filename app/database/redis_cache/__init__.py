import aioredis

from app.config.cfg import RedisCache


def redis_stub():
    """DI function for overwrite dependency returning"""
    raise NotImplementedError


class RedisProvider:
    def __init__(self, cfg: RedisCache):
        self.cfg: RedisCache = cfg
        self.pool = aioredis.ConnectionPool.from_url(
            "redis://{host}:{port}/{db}".format(
                host=self.cfg.host, port=self.cfg.port, db=self.cfg.db_id
            )
        )
        self.redis: aioredis.Redis = aioredis.Redis(
            connection_pool=self.pool, decode_responses=True
        )

    def get_redis(self) -> aioredis.Redis:
        """
        Get Redis object for dependency

        :return: object of aioredis.Redis
        """
        return self.redis
