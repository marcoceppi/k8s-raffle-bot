import asyncio
import os

import discord

from rafflebot.cogs import (
    Hello,
    Raffle,
    RaffleAdmin,
)
from rafflebot.core.bot import RaffleBot
intents = discord.Intents.default()
intents.members = True


def run():
    # Todo: just do when mentioned
    bot = RaffleBot(
        command_prefix=discord.ext.commands.when_mentioned_or("SIG Raffle"),
    )

    bot.add_cog(Raffle(bot))
    bot.add_cog(RaffleAdmin(bot))
    bot.add_cog(Hello(bot))

    bot.run(os.environ.get("DISCORD_TOKEN"))
