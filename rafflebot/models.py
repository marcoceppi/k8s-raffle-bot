import os
from uuid import uuid4

from rafflebot.core.database import Database


class Model:
    prefix = "rafflebot"
    db = Database(os.environ.get("REDIS_URL"))
    model = ""

    def create_id(self):
        return str(uuid4())

    def key(self, record=None):
        _key = f"{self.prefix}.{self.model}"
        if record:
            _key = f"{_key}:{record}"

        return _key


class Settings(Model):
    model = "settings"

    default_settings = {
        "award-interval": 60,
        "last-awarded": None,
    }

    def valid(self, name):
        return name in self.default_settings

    async def update(self, name, value):
        if not self.valid(name):
            return False  # TODO: raise exception

        await self.db.conn.hset(self.key(), name, value)
        return True

    async def list(self):
        settings = await self.db.conn.hgetall(self.key())
        output = self.default_settings.copy()
        output.update(settings)
        return output

    async def get(self, name):
        if not self.valid(name):
            return False  # TODO: raise exception

        value = await self.db.conn.hget(self.key(), name)
        return self.default_settings.get(name) if not value else value


class Prizes(Model):
    model = "prizes"

    async def insert(self, name, code):
        record_id = self.create_id()
        index_key = self.key()

        record_key = self.key(record_id)
        payload = {
            "name": name,
            "code": code,
        }

        await self.db.conn.hmset_dict(record_key, payload)
        await self.db.conn.sadd(index_key, record_id)

    async def list(self, include_members=False):
        indexes = await self.db.conn.smembers(self.key())

        if not include_members:
            return indexes

        members = {}
        for index in indexes:
            members[index] = await self.db.conn.hgetall(self.key(index))

        return members

    async def remove(self, id):
        indexes = await self.list()
        match = None

        for index in indexes:
            index = index
            if index.startswith(id):
                match = index
                break

        if not match:
            return False

        await self.db.conn.delete(self.key(index))
        await self.db.conn.srem(self.key(), index)

        return True
