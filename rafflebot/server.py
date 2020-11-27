import asyncio
import os

import discord

from rafflebot.cogs import (
    Hello,
    Raffle,
    RaffleAdmin,
)
from rafflebot.core.bot import RaffleBot


def run():
    intents = discord.Intents.default()
    intents.members = True
    # Todo: just do when mentioned
    bot = RaffleBot(
        command_prefix=discord.ext.commands.when_mentioned_or("SIG Raffle"),
        intents=intents,
    )

    bot.add_cog(Raffle(bot))
    bot.add_cog(RaffleAdmin(bot))
    bot.add_cog(Hello(bot))

    bot.run(os.environ.get("DISCORD_TOKEN"))
