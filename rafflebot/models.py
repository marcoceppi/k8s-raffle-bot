import os
import time
from uuid import uuid4

import discord

from rafflebot.core.database import Database


class Model:
    db = Database(os.environ.get("REDIS_URL"))
    prefix = "rafflebot"
    model = ""
    guild = None

    def __init__(self, guild: discord.Guild):
        self.guild = guild

    def create_id(self):
        return str(uuid4())

    def key(self, record=None):
        _key = f"{self.prefix}.{self.guild.id}.{self.model}"
        if record:
            _key = f"{_key}:{record}"

        return _key

    async def exists(self, record=None):
        return await self.db.conn.exists(self.key(record))


class Settings(Model):
    model = "settings"

    default_settings = {
        "award-interval": 60,
        "last-awarded": None,
        "awardable-role": None,
        "winner-dm-content": "",
        "winner-announce-channel": None,
        "winner-announce-content": "",
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

    async def remove(self, name):
        if not self.valid(name):
            return False  # TODO: raise exception

        return await self.db.conn.hdel(self.key(), name) is not False


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
            members[index] = await self.get(index)

        return members

    async def get(self, id):
        return await self.db.conn.hgetall(self.key(id))

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


class AwardedPrizes(Model):
    model = "winners.prizes"

    async def insert(self, prize, member):
        if not await Prizes(self.guild).exists(prize):
            return False

        await self.db.conn.hset(self.key(), prize, member)

    def list(self, include_members=False):
        if not include_members:
            return self.db.conn.hkeys(self.key())

        return self.db.conn.hgetall(self.key())


class Winners(Model):
    model = "winners"

    async def insert(self, member, prize, when=None):
        if not await Prizes(self.guild).exists(prize):
            return False

        if not when:
            when = time.time()

        await self.db.conn.zadd(self.key(), when, member)
        await self.db.conn.zadd(self.key(member), when, prize)

        await AwardedPrizes(self.guild).insert(prize, member)

    async def list(self, include_members=False):
        winners = await self.db.conn.zrange(self.key(), 0, -1)

        if not include_members:
            return winners

        output = {}

        for member in winners:
            prizes = await self.db.conn.zrange(self.key(member), 0, -1, withscores=True)

            if member not in output:
                output[member] = []

            for awarded in prizes:
                prize, timestamp = awarded
                output[member].append({"awarded": timestamp, "prize": prize})
        return output
