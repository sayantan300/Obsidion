import logging

from discord.ext import commands

minecraft = [
    "ᔑ",
    "ʖ",
    "ᓵ",
    "↸",
    "ᒷ",
    "⎓",
    "⊣",
    "⍑",
    "╎",
    "⋮",
    "ꖌ",
    "ꖎ",
    "ᒲ",
    "リ",
    "𝙹",
    "!",
    "¡",
    "ᑑ",
    "∷",
    "ᓭ",
    "ℸ",
    " ̣",
    "⚍",
    "⍊",
    "∴",
    " ̇",
    "|",
    "|",
    "⨅",
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
]
alphabet = "abcdefghijklmnopqrstuvwxyz123456789"

log = logging.getLogger(__name__)


class fun(commands.Cog):
    """commands that are bot related"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["villagerspeak", "villagerspeech", "hmm"])
    async def villager(self, ctx: commands.Context, *, speech: str):
        """Convert english to Villager speech hmm."""
        split = speech.split(" ")
        sentence = ""
        for _ in split:
            sentence += " hmm"
        response = sentence.strip()
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    @commands.command()
    async def enchant(self, ctx: commands.Context, *, msg: str):
        """Enchant a message"""
        response = ""
        for letter in msg:
            if letter in alphabet:
                response += minecraft[alphabet.index(letter)]
            else:
                response += letter
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    @commands.command()
    async def unenchant(self, ctx: commands.Context, *, msg: str):
        """Disenchant a message"""
        response = ""
        for letter in msg:
            if letter in minecraft:
                response += alphabet[minecraft.index(letter)]
            else:
                response += letter
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    @commands.command()
    async def creeper(self, ctx):
        """Aw man"""
        await ctx.send("Aw man")
