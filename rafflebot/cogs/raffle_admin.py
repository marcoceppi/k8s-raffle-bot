import datetime

import humanize
from discord.ext import commands

from rafflebot import models
from rafflebot.core import emoji, utils


class RaffleAdmin(commands.Cog, name="Raffle Administration"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add-prize")
    @commands.has_permissions(administrator=True)
    async def add_prize(self, ctx, *args):
        if len(args) != 2:
            return await utils.failure(
                ctx, 'Hi, please let me know the prize name and the redemption code as `"prize name" code`'
            )

        name, code = args
        await models.Prizes(ctx.guild).insert(name, code)
        await utils.success(ctx)

    @commands.command(name="remove-prize")
    @commands.has_permissions(administrator=True)
    async def remove_prize(self, ctx, prize_id):
        if not (await models.Prizes(ctx.guild).remove(prize_id)):
            return await utils.failure(ctx)

        await utils.success(ctx)

    def prize_status(self, prize, awarded_prizes):
        return emoji.emoji_status(prize, awarded_prizes, emoji.PRIZE_AWARDED, emoji.PRIZE_AVAILABLE)

    @commands.command(name="list-prizes")
    @commands.has_permissions(administrator=True)
    async def list_prizes(self, ctx):
        prizes = await models.Prizes(ctx.guild).list(include_members=True)
        awarded_prizes = await models.AwardedPrizes(ctx.guild).list()

        prizes = [
            f"{self.prize_status(k, awarded_prizes)} {val['name']} ({k.split('-')[0]})" for k, val in prizes.items()
        ]
        if prizes:
            await ctx.send("\n".join(prizes))

        await utils.success(ctx)

    @commands.command(name="list-settings")
    @commands.has_permissions(administrator=True)
    async def list_settings(self, ctx):
        settings = await models.Settings(ctx.guild).list()
        settings = [f"{emoji.SETTING} {k}: {v}" for k, v in settings.items()]
        await ctx.send("\n".join(settings))
        await utils.success(ctx)

    @commands.command(name="update-setting")
    @commands.has_permissions(administrator=True)
    async def update_settings(self, ctx: commands.Context, name, *args):
        print(ctx.message.content)
        value = ctx.message.content.split(f"{name} ")[1]
        print(value)
        if not (await models.Settings(ctx.guild).update(name, value)):
            return await utils.failure(ctx)

        await utils.success(ctx)

    @commands.command(name="reset-setting")
    @commands.has_permissions(administrator=True)
    async def reset_settings(self, ctx, name):
        if not (await models.Settings(ctx.guild).remove(name)):
            return await utils.failure(ctx)

        await utils.success(ctx)

    @commands.command(name="list-winners")
    @commands.has_permissions(administrator=True)
    async def list_winners(self, ctx):
        winners = await models.Winners(ctx.guild).list(include_members=True)

        output = []

        for member, prizes in winners.items():
            for p in prizes:
                prize = await models.Prizes(ctx.guild).get(p["prize"])
                awarded = datetime.datetime.fromtimestamp(p["awarded"])
                print(member)

                user = self.bot.get_user(int(member))
                print(user)
                output.append(
                    f"{emoji.PRIZE_WINNER} {user.mention}: **{prize['name']}** ({humanize.naturaltime(datetime.datetime.now() - awarded)})"
                )
        await ctx.send("\n".join(output))
        await utils.success(ctx)
