from discord.ext import commands
from random import choice
import discord
from utils.db import Data
from utils.utils import get_uuid, get


class Configurable(commands.Cog, name="Configurable"):

    def __init__(self, bot):
        self.session = bot.session
        self.bot = bot

    @commands.group(aliases=["acc"])
    async def account(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('No command passed')

    @account.command(name="link")
    async def account_link(self, ctx, username=None):
        if username:
            uuid = await get_uuid(self.session, username)
            if uuid:
                self.bot.pool["user"][str(ctx.author.id)] = {"uuid": uuid}
                Data.save("", self.bot.pool)
                await ctx.send(f"Your account has been linked to {username}")
            else:
                await ctx.send("Please provide a valid username")
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: please provide a username")

    @account.command(name="unlink")
    async def account_unlink(self, ctx):
        self.bot.pool["user"][str(ctx.author.id)] = {"uuid": None}
        Data.save("", self.bot.pool)
        await ctx.send("Your account has been unlinked from any minecraft account")

    @commands.group()
    @commands.has_guild_permissions(administrator=True)
    async def serverlink(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Please pass either `link <server>` or `unlink`')

    @serverlink.command(name="link")
    async def serverlink_link(self, ctx, server):
        self.bot.pool["guilds"][str(ctx.guild.id)]["server"] = server
        Data.save("", self.bot.pool)
        await ctx.send(f"Your discord server has been linked to {server}")

    @serverlink.command(name="unlink")
    async def serverlink_unlink(self, ctx):
        self.bot.pool["guilds"][str(ctx.guild.id)]["server"] = None
        Data.save("", self.bot.pool)
        await ctx.send("Your discord server is no longer linked to a minecraft server")

    @commands.command()
    @commands.has_permissions(administrator=True)
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

    @commands.command(aliases=["strack", "servertracking"])
    @commands.has_guild_permissions(administrator=True)
    async def servertrack(self, ctx, server=None, voiceChannel=None):
        """Server tracking is info"""
        if server:
            if voiceChannel:
                channel = self.bot.get_channel(int(voiceChannel))
                if channel:
                    await channel.edit(name="SERVERTRACKING")
                    data = await get(self.session, f"https://api.mcsrvstat.us/2/{server}")
                    self.bot.pool["serverTracking"][str(ctx.guild.id)] = {
                        "channel": voiceChannel, "server": server}
                    Data.save("", self.bot.pool)
                    if data["online"]:
                        name = f"{server.split('.')[0].title()}: {data['players']['online']:,} / {data['players']['max']:,}"
                        await channel.edit(name=name)
                    else:
                        await channel.edit(name="SERVER IS OFFLINE")
                else:
                    await ctx.send("I cannot find that channel")
            else:
                await ctx.send("Please provide a valid voice server ID")
        else:
            await ctx.send("Please provide a minecraft server")

    #@commands.group()
    #@commands.has_guild_permissions(administrator=True)
    #async def blacklist(self, ctx):
    #    if ctx.invoked_subcommand is None:
    #        embed = discord.Embed(title=f"{self.bot.user.name} Blacklist Command",
    #                              description=f"Blacklisting is a feature that allows you to configure {self.bot.user.name} to ignore certain commands. You can use this to blacklist commands in a certain channel or the whole Discord server. Require assistance? Join the [Support Discord Server](https://discord.gg/7BRD7s6) for help.")
    #        prefix = self.bot.pool["guilds"][str(ctx.guild.id)]["prefix"]
    #        embed.add_field(name="Usage", 
    #                              value=f"`{prefix}blacklist add` - Add a command or category to the blacklist.\n`{prefix}blacklist remove` - Remove a command or category to the blacklist.\n`{prefix}blacklist silent` - Enable or disable replies to blacklisted command usage.\n`{prefix}blacklist settings` - Displays the current configuration.")

    #        await ctx.send(embed=embed)

    #@blacklist.command()
    #async def add(self, ctx, command):
    #    pass

    #@blacklist.command()
    #async def remove(self, ctx, command):
    #    pass

    #@blacklist.command()
    #async def silent(self, ctx):
    #    embed=discord.Embed(title="Silent Blacklist", description=f"Would you like {self.bot.user.mention} to respond when a blacklisted command is used?\nYes or No")
    #    await ctx.send(embed=embed)
    #    def check(m):
    #        print(m.content)
    #        return m.author == ctx.author and m.content.lower() in ["yes", "no"]
    #    try:
    #        msg = await self.bot.wait_for("message", check=check, timeout=30).content.lower()
    #        if msg == "yes":
    #            await ctx.send(":white_check_mark: Silent reply succesfully **enabled**")
    #        else:
    #            await ctx.send(":white_check_mark: Silent reply succesfully **disabled**")
    #    else:
    #        ctx.send(f"{ctx.message.author.mention}, zyou did not respond tot the question, setup has been cancelled.")

    #@blacklist.command()
    #async def settings(self, ctx, command):
    #    pass

    # @command.command()
    # async def configuration(self, ctx):
    #    pass
