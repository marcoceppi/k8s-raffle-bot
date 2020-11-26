import asyncio
import discord
import os

from rafflebot.core.bot import RaffleBot
from rafflebot.cogs import Raffle, RaffleAdmin, Hello


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
