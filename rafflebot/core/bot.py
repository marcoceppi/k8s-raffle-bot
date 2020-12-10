import asyncio

from discord.ext import commands

from rafflebot.core.database import Database
from rafflebot.tasks.award import Award
from rafflebot.core import utils


class RaffleBot(commands.Bot):
    async def on_connect(self):
        await Database("").connect()
        award = Award(self)
        asyncio.create_task(award.run())

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            return await utils.denied(ctx)

        await super().on_command_error(ctx, error)
