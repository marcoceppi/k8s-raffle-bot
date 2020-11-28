import random

import discord
from discord.ext import commands

from rafflebot.core import utils
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

    async def notify_winner(self, member, prize):
        msg = await Settings(member.guild).get("winner-dm-content")

        await member.send(msg.format(guild=member.guild, prize_name=prize["name"], prize_code=prize["code"]))

    async def notify_channel(self, member, prize):
        msg = await Settings(member.guild).get("winner-announce-content")
        channel = await Settings(member.guild).get("winner-announce-channel")
        channel_id = utils.unmentioned(channel)
        channel = self.bot.get_channel(int(channel_id))

        if not msg or not channel:
            return

        await channel.send(
            msg.format(member=member.mention, guild=member.guild, prize_name=prize["name"], prize_code=prize["code"])
        )

    async def notify(self, channel, text):
        pass

    async def award(self, guild: discord.Guild):
        members = await self.get_eligable_members(guild)
        prizes = await self.get_eligable_prizes(guild)
        winner = random.choice(members)
        prize_id = random.choice(prizes)
        prize = await Prizes(guild).get(prize_id)

        await Winners(guild).insert(winner.id, prize_id)

        await self.notify_winner(winner, prize)
        await self.notify_channel(winner, prize)
