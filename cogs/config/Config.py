from discord.ext import commands
from random import choice
import discord

class Configurable(commands.Cog, name="Configurable"):

    @commands.command()
    async def autopost(self, ctx):
        pass

    @commands.command()
    async def serverlink(self, ctx):
        pass

    @commands.command()
    async def account(self, ctx):
        pass

    @commands.command()
    async def blacklist(self, ctx):
        pass

    @commands.command()
    async def configuration(self, ctx):
        pass

    @commands.command()
    async def prefix(self, ctx):
        pass