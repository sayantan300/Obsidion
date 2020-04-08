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
        """view your Obisidon account
        do account link to link a minecraft username"""
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
        """link a minecraft server to your guild
        do serverlink link <server>"""
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
    async def servertrack(self, ctx):
        """Server tracking is info"""
        if not self.bot.pool["guilds"][str(ctx.guild.id)]["serverTracking"]: # check wether servertracking is already setup
            def check(m):
               return m.author == ctx.author
            # get minecraft server
            embed=discord.Embed(title="Server Tracking Setup", description=f"please provide the minecraft server you would like to track")
            await ctx.send(embed=embed)
            server = await self.bot.wait_for("message", check=check, timeout=30)
            server = server.content
            
            # get the voice channel
            voiceChannel=False
            while not voiceChannel:
                embed=discord.Embed(title="Server Tracking Setup", description=f"Please provide the name of the voice channel you would like to use\n I will need to have the permissions to edit the name and everyone else should not be able to join it.")
                await ctx.send(embed=embed)
                voice = await self.bot.wait_for("message", check=check, timeout=30)
                channel = discord.utils.get(ctx.guild.voice_channels, name=voice.content)
                print(channel.id)
                if channel is not None:
                    voiceChannel=channel.id
            self.bot.pool["guilds"][str(ctx.guild.id)]["serverTracking"] = [server, voiceChannel]
            if server in self.bot.pool["serverTracking"]:
                self.bot.pool["serverTracking"][server].append(voiceChannel)
            else:
                self.bot.pool["serverTracking"][server] = [voiceChannel]
            print(self.bot.pool)
            Data.save("", self.bot.pool)
            self.bot.get_channel(int(voiceChannel))
            await channel.edit(name="SERVERTRACKING")
            data = await get(self.session, f"https://api.mcsrvstat.us/2/{server}")
            if data["online"]:
                name = f"{server.split('.')[0].title()}: {data['players']['online']:,} / {data['players']['max']:,}"
                await channel.edit(name=name)
            else:
                await channel.edit(name="SERVER IS OFFLINE")
        else:
            def yes(m):
                return m.author == ctx.author and m.content.lower() in ["yes", "no"]
            await ctx.send("there is a server tracking channel setup already would you like me to remove it?")
            delete = await self.bot.wait_for("message", check=yes, timeout=30)
            if delete.content == "yes":
                server, voiceChannel = self.bot.pool["guilds"][str(ctx.guild.id)]["serverTracking"]
                test = self.bot.pool
                test["guilds"][str(ctx.guild.id)]["serverTracking"] = None
                if len(test["serverTracking"][server]) == 1:
                    diction = test["serverTracking"]
                    diction.pop(server)
                    test["serverTracking"] = diction
                else:
                    test["serverTracking"][server].remove(voiceChannel)
                Data.save("", test)
                self.bot.pool = test
                await ctx.send("your server tracking has been deleted to setup server tracking run the command again")

    # @commands.group()
    # @commands.has_guild_permissions(administrator=True)
    # async def blacklist(self, ctx):
    #     if ctx.invoked_subcommand is None:
    #         embed = discord.Embed(title=f"{self.bot.user.name} Blacklist Command",
    #                               description=f"Blacklisting is a feature that allows you to configure {self.bot.user.name} to ignore certain commands. You can use this to blacklist commands in a certain channel or the whole Discord server. Require assistance? Join the [Support Discord Server](https://discord.gg/7BRD7s6) for help.")
    #         prefix = self.bot.pool["guilds"][str(ctx.guild.id)]["prefix"]
    #         embed.add_field(name="Usage", 
    #                               value=f"`{prefix}blacklist add` - Add a command or category to the blacklist.\n`{prefix}blacklist remove` - Remove a command or category to the blacklist.\n`{prefix}blacklist silent` - Enable or disable replies to blacklisted command usage.\n`{prefix}blacklist settings` - Displays the current configuration.")

    #         await ctx.send(embed=embed)

    # @blacklist.command()
    # async def add(self, ctx, command, channel=None):
    #     if channel:
    #         # Channel specific blacklist
    #         for x in self.bot.cogs:
    #             for y in self.bot.get_cog(x).get_commands():
    #                 if y.name == command:
    #                     found = True
    #                     break
    #         if found:
    #             discord_channel = self.bot.get_channel(int(channel))
    #             if discord_channel:
    #                 if str(str(channel)) in self.bot.pool["blacklist"]:
    #                     self.bot.pool["blacklist"][str(channel)] = self.bot.pool["blacklist"][str(channel)].append(command)
    #                 else:
    #                     self.bot.pool["blacklist"][str(channel)] = [command]
    #                 Data.save("", self.bot.pool)
    #                 await ctx.send(f"{ctx.message.author.mention}, That command has been blacklisted for use in {channel}.")
    #             else:
    #                 await ctx.send(f"{ctx.message.author.mention}, That command has been blacklisted for use in {channel}.")
    #         else:
    #             await ctx.send(f"{ctx.message.author.mention}, :x: That command has not been found please try again.")
    #     else:
    #         #guild wide blacklist
    #         for x in self.bot.cogs:
    #             for y in self.bot.get_cog(x).get_commands():
    #                 if y.name == command:
    #                     found = True
    #                     break
    #         if found:
    #             if str(ctx.message.guild.id) in self.bot.pool["blacklist"]:
    #                 self.bot.pool["blacklist"][str(ctx.message.guild.id)] = self.bot.pool["blacklist"][str(ctx.message.guild.id)].append(command)
    #             else:
    #                 self.bot.pool["blacklist"][str(ctx.message.guild.id)] = [command]
    #             Data.save("", self.bot.pool)
    #             await ctx.send(f"{ctx.message.author.mention}, That command has been blacklisted for use in this guild.")
    #         else:
    #             await ctx.send(f"{ctx.message.author.mention}, :x: That command has not been found please try again.")

    # @blacklist.command()
    # async def remove(self, ctx, command):
    #     pass

    # @blacklist.command()
    # async def silent(self, ctx):
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

    # @blacklist.command()
    # async def settings(self, ctx, command):
    #    pass

    # @command.command()
    # async def configuration(self, ctx):
    #    pass