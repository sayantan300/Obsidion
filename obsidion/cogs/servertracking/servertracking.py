from discord.ext import commands, tasks
import asyncio
from obsidion import constants
from obsidion.utils.utils import get


class servertracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_channels.start()

    def cog_unload(self):
        self.update_channels.cancel()

    @tasks.loop(seconds=300.0)
    async def update_channels(self):
        channel = self.bot.get_channel(698031057005707326)
        server = "hypixel.net"
        url = f"{constants.Bot.api}/server/java"
        payload = {"server": server}

        data = await get(self.bot.http_session, url, payload)
        if data:
            name = f"{server.split('.')[-2].title()}: {data['players']['online']:,} / {data['players']['max']:,}"
            await channel.edit(name=name)
        else:
            await channel.edit(name="SERVER IS OFFLINE")

    @update_channels.before_loop
    async def before_update_channels(self):
        print("waiting...")
        await self.bot.wait_until_ready()
