from discord.ext import commands
import discord
import logging

log = logging.getLogger(__name__)


class minecraft:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def recipie(self, ctx, name):
        pass

    @commands.command()
    async def render_block(self, ctx, block):
        pass

    @commands.command()
    async def item_render(self, ctx, item):
        pass

    @commands.commamd()
    async def command(self, ctx, command):
        pass
