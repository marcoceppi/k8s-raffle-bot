from discord.ext import commands


class Hello(commands.Cog):
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello World")
