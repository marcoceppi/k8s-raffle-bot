import asyncio
import time
from rafflebot.models import Settings, Prizes


class Award:
    def __init__(self, bot):
        self.bot = bot

    async def can_award(self):
        last_run = await Settings().get("last-awarded") or 0
        interval = await Settings().get("award-interval")
        prizes = await Prizes().list()

        if not prizes:
            return False

        if last_run + (int(interval) * 60) > time.time():
            return False

        return True

    async def raffle(self):
        pass

    async def run(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            print("Checking if it's time to award")
            if await self.can_award():
                await self.raffle()  # TODO: Make this a Cog?

            start_time = time.time()
            await asyncio.sleep(60)
            end_time = time.time()
            print(end_time - start_time)
