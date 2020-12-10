import re
from typing import Optional

from rafflebot.core import emoji


class Singleton(type):
    _instance: Optional[type] = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


def success(ctx):
    return react(ctx, reactions=[emoji.SUCCESS, emoji.GOOD_JOB])


def failure(ctx, message=None):
    return react(ctx, message, [emoji.FAILURE, emoji.OH_NO])


def error(ctx, message=None):
    return react(ctx, message, [emoji.WHAT])


def denied(ctx):
    return react(ctx, None, [emoji.FAILURE, emoji.DENIED])


async def react(ctx, message: Optional[str] = None, reactions: Optional[list] = None):
    if message:
        await ctx.send(message)

    reactions = reactions if reactions else []

    for r in reactions:
        await ctx.message.add_reaction(r)


def unmentioned(mentionable: str):
    return re.sub(r"[<>#@]", "", mentionable)
