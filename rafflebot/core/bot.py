import asyncio
from discord.ext import commands
from rafflebot.core.database import Database
from rafflebot.tasks.award import Award


class RaffleBot(commands.Bot):
    async def on_connect(self):
        await Database("").connect()
        award = Award(self)
        asyncio.create_task(award.run())
