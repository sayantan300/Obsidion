from discord.ext import commands
from random import choice
import discord
import logging

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


def load_from_text(file):
    with open(f"cogs/fun/{file}.txt") as f:
        content = f.readlines()
    return [x.strip() for x in content]


class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.bot.pool.fetchval(
            "SELECT serverTrack from guild WHERE id = $1", member.guild.id
        ):
            join = load_from_text("join")
            channel = await self.bot.pool.fetchval(
                "SELECT serverTrack from guild WHERE id = $1", member.guild.id
            )
            await channel.send(choice(join).replace("member", member.mention))

    @commands.command(aliases=["idea", "bidea"])
    async def buildidea(self, ctx):
        """Get an idea for a new idea"""
        await ctx.send(
            f"{ctx.message.author.mention}, here is something cool to build: {choice(load_from_text('build_ideas'))}."
        )  # I am aware of the danger of doing this but I don't have a better ideas

    @commands.command(aliases=["funfact"])
    async def fact(self, ctx, id=None):
        """Get a fact about minecraft"""
        facts = load_from_text("facts")
        if id:
            if int(id) < len(facts):
                fact_choice = facts[int(id)]
            else:
                fact_choice = choice(facts)
                id = str(facts.index(fact_choice))
        else:
            fact_choice = choice(facts)
            id = str(facts.index(fact_choice))

        embed = discord.Embed(
            title=f"Minecraft Fact #{id}", description=fact_choice, color=0x00FF00
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["villagerspeak", "villagerspeech", "hmm"])
    async def villager(self, ctx, *, speech):
        """Convert english to Villager speech hmm."""
        split = speech.split(" ")
        sentence = ""
        for s in split:
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
        """Roll a random number.
        The result will be between 1 and `<number>`.
        `<number>` defaults to 100.
        """
        await ctx.send("Aw man")

    @commands.command(aliases=["slay"])
    async def kill(self, ctx, member=None):
        """Kill that pesky friend in a fun and stylish way"""
        kill_mes = load_from_text("kill")
        if not member:
            member = ctx.message.author.mention
        elif str(member) == f"<@{self.bot.owner_id}>":
            member = ctx.message.author.mention

        await ctx.send(choice(kill_mes).replace("member", member))

    @commands.command(aliases=["battle"])
    async def pvp(self, ctx, member1, member2=None):
        """Duel someone"""
        pvp_mes = load_from_text("pvp")
        if member1:
            if not member2:
                member2 = ctx.message.author.mention

            await ctx.send(
                choice(pvp_mes).replace("member1", member1).replace("member2", member2)
            )
        else:
            await ctx.send("Please provide 2 people to fight")
        pass

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
                    f"That is an invalid option can you please choose from rock, paper or shears"
                )
        else:
            await ctx.send(
                f"That is an invalid option can you please choose from rock, paper or shears"
            )
