from discord.ext import commands
from random import choice
import discord
import json


class Configurable(commands.Cog, name="Configurable"):

    # @commands.command()
    # async def autopost(self, ctx):
    #    pass

    # @commands.command()
    # async def serverlink(self, ctx):
    #    pass

    # @commands.command()
    # async def account(self, ctx):
    #    pass

    # @commands.command()
    # async def blacklist(self, ctx):
    #    pass

    # @commands.command()
    # async def configuration(self, ctx):
    #    pass

    @commands.command()
    async def prefix(self, ctx, new_prefix):
        """Set a custom prefix for the bot commands"""
        with open("data.json", "r+") as f:
            json_data = json.load(f)

        cur_prefix = json_data["server"][str(ctx.guild.id)]

        if cur_prefix == new_prefix:
            await ctx.send(f"{ctx.author}, :ballot_box_with_cross: You are already using that as your set prefix for this guild.`")
        else:
            with open("data.json", "r+") as f:
                json_data = json.load(f)
                json_data["server"][str(ctx.guild.id)] = new_prefix
                f.seek(0)
                json.dump(json_data, f, indent=4)
                f.truncate()
            await ctx.send(f"{ctx.author}, :ballot_box_with_check: The prefix has been changed to `{new_prefix}`")
