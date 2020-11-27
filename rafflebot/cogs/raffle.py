import random

import discord
from discord.ext import commands

from rafflebot.models import (
    AwardedPrizes,
    Prizes,
    Settings,
    Winners,
)


class Raffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_eligable_members(self, guild: discord.Guild):
        awardable_role = await Settings(guild).get("awardable-role")
        members = None

        if awardable_role:
            for role in guild.roles:
                if role.mention == awardable_role:
                    members = role.members

        return [member for member in (members or guild.members) if not member.bot]

    async def get_eligable_prizes(self, guild: discord.Guild):
        all_prizes = await Prizes(guild).list()
        awarded_prizes = await AwardedPrizes(guild).list()

        return [prize for prize in all_prizes if prize not in awarded_prizes]

    async def award(self, guild: discord.Guild):
        members = await self.get_eligable_members(guild)
        prizes = await self.get_eligable_prizes(guild)
        winner = random.choice(members)
        prize_id = random.choice(prizes)

        prize = await Prizes(guild).get(prize_id)

        await Winners(guild).insert(winner.id, prize_id)

        name = prize["name"]
        code = prize["code"]

        msg = await Settings(guild).get("winner-dm-content")
        await winner.send(msg.format(guild=guild, prize_name=name, prize_code=code))
