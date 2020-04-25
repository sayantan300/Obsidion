from discord.ext import commands
from random import choice
import discord
import logging
from utils.utils import load_from_text

log = logging.getLogger(__name__)

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


class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot
        self.facts = load_from_text("facts")
        self.kill_mes = load_from_text("kill")
        self.pvp_mes = load_from_text("pvp")

    @commands.command(aliases=["idea", "bidea"])
    async def buildidea(self, ctx):
        """Get an idea for a new idea"""
        await ctx.send(
            f"{ctx.message.author.mention}, here is something cool to build: {choice(load_from_text('build_ideas'))}."
        )

    @commands.command(aliases=["funfact"])
    async def fact(self, ctx, id: int = None):
        """Get a fact about minecraft"""
        if id:
            if id < len(self.facts):
                fact_choice = self.facts[id]
            else:
                await ctx.send(
                    f"We only have {len(self.facts)-1} facts so please choose from this number."
                )
                fact_choice = choice(self.facts)
                id = self.facts.index(fact_choice)
        else:
            fact_choice = choice(self.facts)
            id = self.facts.index(fact_choice)

        embed = discord.Embed(
            title=f"Minecraft Fact #{id}", description=fact_choice, color=0x00FF00
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["villagerspeak", "villagerspeech", "hmm"])
    async def villager(self, ctx, *, speech: str):
        """Convert english to Villager speech hmm."""
        split = speech.split(" ")
        sentence = ""
        for _ in split:
            sentence += " hmm"
        response = sentence.strip()
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

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
        """Unenchant a message"""
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

    @commands.command(aliases=["slay"])
    async def kill(self, ctx, member=None):
        """Kill that pesky friend in a fun and stylish way"""
        if not member:
            member = ctx.message.author.mention
        elif (
            str(member) == f"<@{self.bot.owner_id}>"
            or str(member) == f"<@!{self.bot.owner_id}>"
        ):  # owner protection
            member = ctx.message.author.mention

        await ctx.send(choice(self.kill_mes).replace("member", member))

    @commands.command(aliases=["battle"])
    async def pvp(self, ctx, member1=None, member2=None):
        """Duel someone"""
        if member1:
            if not member2:
                member2 = ctx.message.author.mention

            await ctx.send(
                choice(self.pvp_mes)
                .replace("member1", member1)
                .replace("member2", member2)
            )
        else:
            await ctx.send("Please provide 2 people to fight")

    @commands.command()
    async def rps(self, ctx, user_choice=None):
        """play Rock Paper Shears"""
        if user_choice:
            options = ["rock", "paper", "shears"]
            if user_choice in options:
                c_choice = choice(options)
                if user_choice == options[options.index(user_choice) - 1]:
                    await ctx.send(
                        f"You chose {user_choice}, I chose {c_choice} I win."
                    )
                elif c_choice == user_choice:
                    await ctx.send(
                        f"You chose {user_choice}, I chose {c_choice} looks like we have a tie."
                    )
                else:
                    await ctx.send(
                        f"You chose {user_choice}, I chose {c_choice} you win."
                    )
            else:
                await ctx.send(
                    "That is an invalid option can you please choose from rock, paper or shears"
                )
        else:
            await ctx.send(
                "That is an invalid option can you please choose from rock, paper or shears"
            )
