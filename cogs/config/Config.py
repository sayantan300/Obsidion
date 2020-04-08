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
            embed=discord.Embed(title="Server Tracking Setup", description=f"please provide the minecraft server you would like to track", color=0x00ff00)
            await ctx.send(embed=embed)
            server = await self.bot.wait_for("message", check=check, timeout=10)
            server = server.content
            
            # get the voice channel
            voiceChannel=False
            while not voiceChannel:
                embed=discord.Embed(title="Server Tracking Setup", description=f"Please provide the name of the voice channel you would like to use\n I will need to have the permissions to edit the name and everyone else should not be able to join it.")
                await ctx.send(embed=embed)
                voice = await self.bot.wait_for("message", check=check, timeout=10)
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
            await ctx.send("Server Tracking is all setup and ready for you to enjoy. It will update it less than 5 minutes.")
        else:
            def yes(m):
                return m.author == ctx.author and m.content.lower() in ["yes", "no"]
            await ctx.send("Server Tracking is currently setup would you like me to remove the current configuration?")
            delete = await self.bot.wait_for("message", check=yes, timeout=10)
            if delete.content == "yes":
                server, voiceChannel = self.bot.pool["guilds"][str(ctx.guild.id)]["serverTracking"]
                self.bot.pool["guilds"][str(ctx.guild.id)]["serverTracking"] = None
                if len(self.bot.pool["serverTracking"][server]) == 1:
                    diction = self.bot.pool["serverTracking"]
                    diction.pop(server)
                    self.bot.pool["serverTracking"] = diction
                else:
                    self.bot.pool["serverTracking"][server].remove(voiceChannel)
                Data.save("", self.bot.pool)
                self.bot.pool = self.bot.pool
                await ctx.send("Server Tracking has been removed from this server, run the command again to set it up.")

    @commands.command()
    async def delete(self, ctx):
        """This will delete all data that is linked to your account"""
        embed = discord.Embed(title="DELETE DATA", description="WARNING\n THIS IS AN IRREVERABLE ACTION AND WILL DELETE ALL DATA LINKED TO YOUR ACCOUNT\nDO YOU WISH TO PROCEED?\nYES/NO", colour=0xff0000)
        await ctx.send(embed=embed)
        def yes(m):
            return m.author == ctx.author and m.content.lower() in ["yes", "no"]
        delete = await self.bot.wait_for("message", check=yes, timeout=10)
        if delete.content.lower() == "yes":
            # deletes data
            self.bot.pool["user"].pop(str(ctx.author.id))
            Data.save("", self.bot.pool)
            await ctx.send(f"{ctx.message.author.mention}, all data linked to yuor discord account has been deleted.")
    
    @commands.group()
    @commands.has_guild_permissions(administrator=True)
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=f"{self.bot.user.name} Blacklist Command",
                                  description=f"Blacklisting is a feature that allows you to configure {self.bot.user.name} to ignore certain commands. You can use this to blacklist commands in a certain channel or the whole Discord server. Require assistance? Join the [Support Discord Server](https://discord.gg/7BRD7s6) for help.")
            prefix = self.bot.pool["guilds"][str(ctx.guild.id)]["prefix"]
            embed.add_field(name="Usage", 
                                  value=f"`{prefix}blacklist add` - Add a command or category to the blacklist.\n`{prefix}blacklist remove` - Remove a command or category to the blacklist.\n`{prefix}blacklist silent` - Enable or disable replies to blacklisted command usage.\n`{prefix}blacklist settings` - Displays the current configuration.")

            await ctx.send(embed=embed)

    @blacklist.command()
    async def add(self, ctx, command, channel: discord.TextChannel = None):
        # find command
        found = False
        for x in self.bot.cogs:
            for y in self.bot.get_cog(x).get_commands():
                if y.name == command and y.hidden == False:
                    found = True
                    break
        if found:
            if channel:
                if ctx.message.guild.id not in self.bot.pool["blacklist"]:
                    self.bot.pool["blacklist"][str(ctx.message.guild.id)] = {command: channel.id}
                else:
                    self.bot.pool["blacklist"][str(ctx.message.guild.id)][command] = channel.id
                Data.save("", self.bot.pool)
                await ctx.send(f"{ctx.message.author.mention}, That command has been blacklisted for use in {channel}")
            else:
                if str(ctx.message.guild.id) not in self.bot.pool["blacklist"]:
                    self.bot.pool["blacklist"][str(ctx.message.guild.id)] = {command: "All"}
                else:
                    self.bot.pool["blacklist"][str(ctx.message.guild.id)][command] = "All"
                Data.save("", self.bot.pool)
                await ctx.send(f"{ctx.message.author.mention}, That command has been blacklisted for use in this guild.")
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: That command has not been found please try again.")

    @blacklist.command()
    async def remove(self, ctx, command=None):
        if command in self.bot.pool["blacklist"][str(ctx.guild.id)]:
            self.bot.pool["blacklist"][str(ctx.guild.id)].pop(command)
            Data.save("", self.bot.pool)
            await ctx.send(f"{ctx.message.author.mention}, The command has been removed from the blacklist.")
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: The command was not in the blacklist.")

    @blacklist.command()
    async def silent(self, ctx):
        embed=discord.Embed(title="Silent Blacklist", description=f"Would you like {self.bot.user.mention} to respond when a blacklisted command is used?\nYes or No")
        await ctx.send(embed=embed)
        def check(m):
            return m.author == ctx.author and m.content.lower() in ["yes", "no"]
        msg = await self.bot.wait_for("message", check=check, timeout=30)
        msg = msg.content.lower()
        if msg == "yes":
            self.bot.pool["guilds"][str(ctx.guild.id)]["silent"] = False
            await ctx.send(":white_check_mark: Silent reply succesfully **enabled**")
        else:
            self.bot.pool["guilds"][str(ctx.guild.id)]["silent"] = True
            await ctx.send(":white_check_mark: Silent reply succesfully **disabled**")


    @blacklist.command()
    async def settings(self, ctx):
        embed = discord.Embed(title="Command blacklist settings")
        silent = "Disabled" if self.bot.pool["guilds"][str(ctx.guild.id)]["silent"] else "Enabled"
        embed.add_field(name="Silent reply", value=f"**{silent}**\nWhen enabled, {self.bot.user.name} will not reply to blacklisted commands when they're used.")
        commands = ""
        for command, blacklist_set in self.bot.pool["blacklist"][str(ctx.guild.id)].items():
            commands += f"`{command}` - Guild wide" if blacklist_set == "All" else f"`{command}` - {self.bot.get_channel(blacklist_set)}"
        
        if commands == "":
            commands = "You don't have any commands currently blacklisted."

        embed.add_field(name="Blacklisted Commands", value=commands)

        await ctx.send(embed=embed)