from discord.ext import commands
import discord
import logging
from math import floor, ceil

log = logging.getLogger(__name__)

comparator_stats = {"chest": {}}


class Redstone(commands.Cog, name="Redstone"):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @commands.command()
    async def chest(self, ctx, items: int):
        """calculate how many chests you need for that number of items"""
        await ctx.send(f"you need {round(items/(64*54)+1, None): ,} chests")

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
