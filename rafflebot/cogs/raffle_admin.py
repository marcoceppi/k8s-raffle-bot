from discord.ext import commands

from rafflebot import models
from rafflebot.core import utils


class RaffleAdmin(commands.Cog):
    @commands.command(name="add-prize")
    async def add_prize(self, ctx, *args):
        if len(args) != 2:
            return await utils.failure(
                ctx, 'Hi, please let me know the prize name and the redemption code as `"prize name" code`'
            )

        name, code = args
        await models.Prizes().insert(name, code)

        await utils.success(ctx)

    @commands.command(name="remove-prize")
    async def remove_prize(self, ctx, prize_id):
        if not (await models.Prizes().remove(prize_id)):
            return await utils.failure(ctx)

        await utils.success(ctx)

    @commands.command(name="list-prizes")
    async def list_prizes(self, ctx):
        prizes = await models.Prizes().list(include_members=True)

        prizes = [f"✨ {val['name']} ({k.split('-')[0]})" for k, val in prizes.items()]
        if prizes:
            await ctx.send("\n".join(prizes))

        await utils.success(ctx)

    @commands.command(name="list-settings")
    async def list_settings(self, ctx):
        settings = await models.Settings().list()
        settings = [f"🛠 {k}: {v}" for k, v in settings.items()]
        await ctx.send("\n".join(settings))
        await utils.success(ctx)

    @commands.command(name="update-setting")
    async def update_settings(self, ctx, name, value):
        if not (await models.Settings().update(name, value)):
            return utils.failure(ctx)

        await utils.success(ctx)

    @commands.command(name="reset-setting")
    async def reset_settings(self, ctx, name):
        default_value = models.Settings.default_settings.get(name)

        if not default_value:
            return utils.failure(ctx)

        await self.update_settings(ctx, name, default_value)
