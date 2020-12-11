import asyncio
import time

from rafflebot.models import Prizes, Settings


class Award:
    def __init__(self, bot):
        self.bot = bot

    def can_award(self, last_run, interval, prizes):
        interval = interval or 0

        if not prizes:
            return False

        if float(last_run) + (int(interval) * 60) > time.time():
            return False

        return True

    async def process(self, guild):
        cog = self.bot.get_cog("Raffle")
        settings = Settings(guild)

        enabled = await settings.get("enabled")
        if not enabled:
            return

        last_run = await settings.get("last-awarded") or 0
        interval = await settings.get("award-interval")

        prizes = await cog.get_eligable_prizes(guild)

        if self.can_award(last_run, interval, prizes):
            winner = await cog.run(guild)
            if winner:
                await settings.update("last-awarded", time.time())

    async def run(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            print("Processing...")
            for guild in self.bot.guilds:
                asyncio.create_task(self.process(guild))
                # We eventually want to care about these?

            await asyncio.sleep(10)
