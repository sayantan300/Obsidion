from discord.ext import commands
from random import choice
import discord

minecraft = ["ᔑ", "ʖ", "ᓵ", "↸", "ᒷ", "⎓", "⊣", "⍑", "╎", "⋮", "ꖌ", "ꖎ", "ᒲ", "リ", "𝙹", "!", "¡", "ᑑ", "∷", "ᓭ", "ℸ", " ̣", "⚍", "⍊", "∴", " ̇", "|", "|", "⨅", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
alphabet = "abcdefghijklmnopqrstuvwxyz123456789"

class Fun(commands.Cog, name="Fun"):

    def __init__(self, bot):
        self.bot = bot
        with open("cogs/fun/kill.txt") as f:
            content = f.readlines()
        self.kill = [x.strip() for x in content]
        with open("cogs/fun/pvp.txt") as f:
            content = f.readlines()
        self.pvp = [x.strip() for x in content]

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

    @commands.command()
    async def unenchant(self, ctx, *, msg):
        """Enchant a message"""
        response = ""
        for letter in msg:
            if letter in minecraft:
                response += alphabet[minecraft.index(letter)]
            else:
                response += letter
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    @commands.command()
    async def creeper(self, ctx):
        """Well there is never not enough room for this"""
        await ctx.send("Aw man")

    @commands.command()
    async def kill(self, ctx, member=None):
        """Kill that pesky friend in a fun and stylish way"""
        if not member:
            member = ctx.message.author.mention
        elif str(member) == f"<@{self.bot.owner_id}>":
            member = ctx.message.author.mention

        await ctx.send(eval(f'f"""{choice(self.kill)}"""')) # I am aware of the danger of doing this but I don't have a better ideas

    @commands.command()
    async def pvp(self, ctx, member1, member2=None):
        """Duel someone"""
        if member1:
            if not member2:
                member2 = ctx.message.author.mention

            await ctx.send(eval(f'f"""{choice(self.pvp)}"""')) # Please don't crucify me for doing this
        else:
            await ctx.send("Please provide 2 people to fight")
        pass

    #@commands.command()
    #async def rps(self, ctx):
     #   pass