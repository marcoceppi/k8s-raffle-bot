from discord.ext import commands

from rafflebot import models
from rafflebot.core import utils


class RaffleAdmin(commands.Cog, name="Raffle Administration"):
    @commands.command(name="add-prize")
    async def add_prize(self, ctx, *args):
        if len(args) != 2:
            return await utils.failure(
                ctx, 'Hi, please let me know the prize name and the redemption code as `"prize name" code`'
            )

        name, code = args
        await models.Prizes(ctx.guild).insert(name, code)
        await utils.success(ctx)

    @commands.command(name="remove-prize")
    async def remove_prize(self, ctx, prize_id):
        if not (await models.Prizes(ctx.guild).remove(prize_id)):
            return await utils.failure(ctx)

        await utils.success(ctx)

    @commands.command(name="list-prizes")
    async def list_prizes(self, ctx):
        prizes = await models.Prizes(ctx.guild).list(include_members=True)

        prizes = [f"✨ {val['name']} ({k.split('-')[0]})" for k, val in prizes.items()]
        if prizes:
            await ctx.send("\n".join(prizes))

        await utils.success(ctx)

    @commands.command(name="list-settings")
    async def list_settings(self, ctx):
        settings = await models.Settings(ctx.guild).list()
        settings = [f"🛠 {k}: {v}" for k, v in settings.items()]
        await ctx.send("\n".join(settings))
        await utils.success(ctx)

    @commands.command(name="update-setting")
    async def update_settings(self, ctx: commands.Context, name, *args):
        print(ctx.message.content)
        value = ctx.message.content.split(f"{name} ")[1]
        print(value)
        if not (await models.Settings(ctx.guild).update(name, value)):
            return await utils.failure(ctx)

        await utils.success(ctx)

    @commands.command(name="reset-setting")
    async def reset_settings(self, ctx, name):
        if not (await models.Settings(ctx.guild).remove(name)):
            return await utils.failure(ctx)

        await utils.success(ctx)
