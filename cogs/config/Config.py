from discord.ext import commands
from random import choice
import discord
from utils.db import Data

class Configurable(commands.Cog, name="Configurable"):

    def __init__(self, bot):
        self.session = bot.session
        self.bot = bot

    # @commands.command()
    # async def autopost(self, ctx):
    #    pass

    
    # @commands.command()
    # async def configuration(self, ctx):
    #    pass

    @commands.command()
    async def prefix(self, ctx, new_prefix):
        """Set a custom prefix for the bot commands"""
        cur_prefix = self.bot.pool["guilds"][str(ctx.guild.id)]["prefix"]

        if cur_prefix == new_prefix:
            await ctx.send(f"{ctx.author}, :ballot_box_with_cross: You are already using that as your set prefix for this guild.`")
        else:
            data = self.bot.pool
            data["guilds"][str(ctx.guild.id)]["prefix"] = new_prefix
            Data.save("", data)
            self.bot.pool["guilds"][str(ctx.guild.id)]["prefix"] = new_prefix
            await ctx.send(f"{ctx.author}, :ballot_box_with_check: The prefix has been changed to `{new_prefix}`")