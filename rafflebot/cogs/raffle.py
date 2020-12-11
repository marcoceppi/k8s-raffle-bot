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
        winners = [int(id) for id in await Winners(guild).list()]

        if awardable_role:
            for role in guild.roles:
                if role.mention == awardable_role:
                    members = role.members

        return [member for member in (members or guild.members) if not member.bot and member.id not in winners]

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

        if not msg or not channel:
            return

        channel_id = utils.unmentioned(channel)
        channel = self.bot.get_channel(int(channel_id))

        await channel.send(
            msg.format(member=member.mention, guild=member.guild, prize_name=prize["name"], prize_code=prize["code"])
        )

    async def pick_a_winner(self, guild: discord.Guild):
        members = await self.get_eligable_members(guild)
        return None if not members else random.choice(members)

    async def pick_a_prize(self, guild: discord.Guild):
        prizes = await self.get_eligable_prizes(guild)
        return None if not prizes else random.choice(prizes)

    async def run(self, guild: discord.Guild):
        winner = await self.pick_a_winner(guild)
        prize = await self.pick_a_prize(guild)

        if not winner or not prize:
            return

        await self.award(winner, prize)

        return winner

    async def award(self, winner: discord.Member, prize_id: str):
        guild = winner.guild
        prize = await Prizes(guild).get(prize_id)

        await Winners(guild).insert(winner.id, prize_id)

        await self.notify_winner(winner, prize)
        await self.notify_channel(winner, prize)

    @commands.command(name="run-raffle", help="Start the raffle process outside of the timer!")
    @commands.has_permissions(administrator=True)
    async def run_raffle(self, ctx):
        winner = await self.run(ctx.guild)
        if not winner:
            await ctx.send(f"Unable to raffle - either no eligable members or no prizes")
        else:
            await ctx.send(f"Raffle complete - {winner} has won!")
        await utils.success(ctx)
