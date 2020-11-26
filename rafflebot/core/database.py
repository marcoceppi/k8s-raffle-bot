import aioredis
import asyncio
import importlib

from rafflebot.core.utils import Singleton
from rafflebot.core.exceptions import EngineNotFound


# I may have gone off the deep end combining a singleton and a factory
class Database(metaclass=Singleton):
    def __init__(self, url, engine="redis"):
        engine = self._get_engine(engine)
        self.engine = engine(url)

    def _get_engine(self, engine):
        mod = importlib.import_module("rafflebot.core.database")
        clsname = f"{engine.capitalize()}Engine"
        try:
            cls = getattr(mod, clsname)
        except AttributeError:
            raise EngineNotFound(f"{clsname} is not a valid Engine")

        return cls

    def __getattr__(self, k):
        return getattr(self.engine, k)


class EngineBase:
    conn = None

    def __init__(self, url, autoconnect=False):
        self.url = url
        if autoconnect:
            asyncio.create_task(self.connect())

    async def connect(self):
        raise NotImplementedError()

    async def close(self):
        raise NotImplementedError()


class RedisEngine(EngineBase):
    async def connect(self):
        self.conn = await aioredis.create_redis_pool(self.url, encoding="utf8")

    async def close(self):
        self.conn.close()
        await self.conn.wait_closed()
