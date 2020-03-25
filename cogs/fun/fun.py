from discord.ext import commands
from random import choice
import discord

class Fun(commands.Cog, name="Fun"):

    @commands.command()
    async def enchant(self, ctx):
        pass

    @commands.command()
    async def fact(self, ctx):
        pass

    @commands.command()
    async def trivia(self, ctx):
        pass

    @commands.command()
    async def tntsweeper(self, ctx):
        pass

    @commands.command()
    async def creeper(self, ctx):

        await ctx.send("Aw man")

    @commands.command()
    async def kill(self, ctx):

        killing = [" was shot by a skeleton using a bow.", " was struck by lightning.", " turned into dust.", " was ripped apart by a Vex."]

        await ctx.send(ctx.author + choice(killing))

    @commands.command()
    async def pvp(self, ctx):
        pass

    @commands.command()
    async def rps(self, ctx):
        pass