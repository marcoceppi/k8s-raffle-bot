import os
import sys
import discord

client = discord.Client()
total = 1

if len(sys.argv) == 2:
    total = int(sys.argv[1])


@client.event
async def on_ready():
    channel = client.get_channel(775037369447350275)
    for _ in range(500):
        invite = await channel.create_invite(
            max_uses=5, reason="Invite for attendees of the K8S Contributor Celebration"
        )
        print(invite.url)


client.run(os.environ.get("DISCORD_TOKEN"))
