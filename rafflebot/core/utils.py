import re
from typing import Optional

from rafflebot.core import emoji


class Singleton(type):
    _instance: Optional[type] = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


async def success(ctx):
    await ctx.message.add_reaction(emoji.SUCCESS)
    await ctx.message.add_reaction(emoji.GOOD_JOB)


async def failure(ctx, message=None):
    if message:
        await ctx.send(message)

    await ctx.message.add_reaction(emoji.FAILURE)
    await ctx.message.add_reaction(emoji.OH_NO)


def unmentioned(mentionable: str):
    return re.sub(r"[<>#@]", "", mentionable)
