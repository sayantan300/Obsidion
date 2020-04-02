import discord
from discord.ext import commands
import aiohttp
import datetime
import asyncio
from utils.utils import get_uuid

class servers(commands.Cog, name="Servers"):

    def __init__(self, bot):
        self.session = bot.session
        self.bot = bot
        self.hypixel = bot.hypixel_api

    #@commands.command()
    #async def blocksmcself(self, ctx, username):
    #    pass

    #@commands.command()
    #async def funcraft(self, ctx, username):
    #    pass

    #async def hivemc(self, ctx, username):
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