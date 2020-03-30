from discord.ext import commands
from random import choice
import discord

minecraft = "ᔑʖᓵ↸ᒷ⎓⊣⍑╎⋮ꖌꖎᒲリ𝙹!¡ᑑ∷ᓭℸ ̣⚍⍊∴ ̇/||⨅"
alphabet = "abcdefghijklmnopqrstuvwxyz"

class Fun(commands.Cog, name="Fun"):

    @commands.command()
    async def enchant(self, ctx, *, msg):
        """Enchant a message"""
        response = ""
        for letter in msg:
            if letter in alphabet:
                response += minecraft[alphabet.index(letter)]
            else:
                response += letter
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    #@commands.command()
    #async def tntsweeper(self, ctx):
    #    pass

    @commands.command()
    async def creeper(self, ctx):
        """Well there is never not enough room for this"""
        await ctx.send("Aw man")

    @commands.command()
    async def kill(self, ctx, member=None):
        """Kill that pesky friend in a fun and stylish way"""
        if not member:
            member = ctx.message.author.mention

        killing = ["was shot by a skeleton using a bow.", "was struck by lightning.", "turned into dust.", "was ripped apart by a Vex.", "tripped too hard and died.", "was squashed by a falling block.", "was killed by gravity.", "failed at killing a Creeper.", "had one to many speed potions.", "was ripped apart by a Spider Jockey."]

        await ctx.send(f"{member} {choice(killing)}")

    #@commands.command()
    #async def pvp(self, ctx):
    #    pass

    #@commands.command()
    #async def rps(self, ctx):
     #   pass