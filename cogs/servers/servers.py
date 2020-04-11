import discord
from discord.ext import commands
import aiohttp
import datetime
import asyncio
from utils.utils import get_uuid, get
from mcstatus import MinecraftServer


class servers(commands.Cog, name="Servers"):
    def __init__(self, bot):
        self.session = bot.session
        self.bot = bot

        # servertracking as a background task
        self.bg_task = bot.loop.create_task(self.my_background_task())

    async def my_background_task(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for server, channel, guild in await self.bot.pool.fetch(
                "SELECT * FROM servertracking"
            ):
                # loop through every minecraft server
                try:
                    mc_server = MinecraftServer.lookup(server)
                    data = mc_server.status()
                except:
                    data = False
                channel = self.bot.get_channel(channel)
                # check
                if data:
                    name = f"{server.split('.')[-2].title()}: {data.players.online:,} / {data.players.max:,}"
                    await channel.edit(name=name)
                else:
                    await channel.edit(name="SERVER IS OFFLINE")
            await asyncio.sleep(5 * 60)  # task runs every 5 minutes

    # @commands.command()
    # async def blocksmcself(self, ctx, username):
    #    pass

    # @commands.command()
    # async def funcraft(self, ctx, username):
    #    pass

    # async def hivemc(self, ctx, username):
    #    pass


'''
    @commands.command()
    async def hypixel(self, ctx, username):
        """Get information about a Hypixel user"""
        pass
            

    #@commands.command()
    #async def manacube(self, ctx, username):
    #    pass

    #@commands.command()
    #async def minesage(self, ctx, username):
    #    pass

    #@commands.command()
    #async def universocraft(self, ctx, username):
    #    pass

    #@commands.command()
    #async def veltpvp(self, ctx, username):
    #    pass

    #@commands.command()
    #async def wynncraft(self, ctx, username):
    #    uuid = get_uuid(self.session, username)
    #    if uuid:
    #        url = f"https://api.wynncraft.com/v2/player/{uuid}/stats"
    #        data = await get(self.session, url)

    #        embed = discord.Embed(color=0x00ff00)
    #        
    #        information = ""

    #        dates = ""
    #        dates += f"First Login: `{data['meta']['firstJoin']}`\n"
    #        dates += f"Last Login: `{data['meta']['lastJoin']}`"
    #        dates += f"Playtime: `{data['meta']['playtime']}`"

    #        await ctx.send(embed=embed)
    #    pass
'''
