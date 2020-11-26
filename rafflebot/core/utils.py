from typing import Optional


class Singleton(type):
    _instance: Optional[type] = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


async def success(ctx):
    await ctx.message.add_reaction("✨")
    await ctx.message.add_reaction("👍")


async def failure(ctx, message=None):
    if message:
        await ctx.send(message)

    await ctx.message.add_reaction("🔴")
    await ctx.message.add_reaction("😭")
