from discord.ext import commands
from random import choice
import discord
from utils.db import Data
from utils.utils import get_uuid

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
    async def account(self, ctx, command, username=None):
        if command in ["unlink", "link"]:
            if command == "unlink":
                self.bot.pool["user"][str(ctx.author.id)] = {"uuid": None}
                Data.save("", self.bot.pool)
                await ctx.send("Your account has been unlinked from any minecraft account")
            else:
                if username:
                    uuid = await get_uuid(self.session, username)
                    if uuid:
                        self.bot.pool["user"][str(ctx.author.id)] = {"uuid": uuid}
                        Data.save("", self.bot.pool)
                        await ctx.send(f"Your account has been linked to {username}")
                    else:
                        await ctx.send("Please provide a valid username")
                else:
                    await ctx.send("Please provide a username")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def serverlink(self, ctx, server=None):
        if server:
            self.bot.pool["guilds"][str(ctx.guild.id)]["server"] = server
            Data.save("", self.bot.pool)
            await ctx.send(f"Your discord server has been linked to {server}")
        else:
            ctx.send("Please provide a server to link to")


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