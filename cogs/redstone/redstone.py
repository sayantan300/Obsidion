from discord.ext import commands
import logging
from math import floor, ceil
import re
import itertools

log = logging.getLogger(__name__)

comparator_stats = {"chest": {}}


class Redstone(commands.Cog, name="Redstone"):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @commands.command()
    async def chest(self, ctx, items: int):
        """calculate how many chests you need for that number of items"""
        chest_count = round(items / (64 * 54) + 1, None)

        if chest_count > 1:
            double_chests = int(chest_count / 2)
            single_chests = chest_count % 2
            await ctx.send(
                f"You need {double_chests} double chests and {single_chests} chest or {chest_count} shulkers"
            )
        else:
            await ctx.send(
                f"you need {round(items/(64*54)+1, None): ,} chest or shulker box"
            )

    @commands.command()
    async def comparator(self, ctx, item_count: int):
        """calculate the strength of a comparator output only works for a chest"""
        signal_strength = floor(1 + ((item_count / 64) / 54) * 14)
        await ctx.send(f"Comparator output of {signal_strength}")

    @commands.command()
    async def itemsfromredstone(self, ctx, item_count: int):
        """calculate the strength of a comparator output only works for a chest"""
        signal_strength = max(item_count, ceil((54 * 64 / 14) * (item_count - 1)))
        await ctx.send(f"You need at least {signal_strength} items")

    @commands.command()
    async def tick2second(self, ctx, ticks: int):
        """Convert seconds to tick"""
        seconds = ticks / 20
        await ctx.send(f"It takes {seconds} second for {ticks} to happen.")

    @commands.command()
    async def second2tick(self, ctx, seconds: float):
        """Convert ticks to seconds"""
        ticks = seconds * 20
        await ctx.send(f"There are {ticks} ticks in {seconds} seconds")

    @commands.command()
    async def minecraftformat(self, ctx, *, text):
        """format discord markdown into minecraft text formating"""
        # underline
        if "__" in text:
            text = re.sub(
                "(__)",
                lambda m, c=itertools.count(): m.group() if next(c) % 5 else "§n",
                text,
            ).replace("__", "§r")

        # bold
        if "**" in text:
            text = re.sub(
                "(**)",
                lambda m, c=itertools.count(): m.group() if next(c) % 5 else "§l",
                text,
            ).replace("**", "§r")

        # italic
        if "*" in text:
            text = re.sub(
                "(*)",
                lambda m, c=itertools.count(): m.group() if next(c) % 5 else "§l",
                text,
            ).replace("*", "§r")

        # strikethrough
        if "~~" in text:
            text = re.sub(
                "(~~)",
                lambda m, c=itertools.count(): m.group() if next(c) % 5 else "§m",
                text,
            ).replace("~~", "§r")

        await ctx.send(text)
