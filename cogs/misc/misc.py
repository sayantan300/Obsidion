from discord.ext import commands
from random import choice
import discord
import resource
import aiohttp
import datetime
import time


class Miscellaneous(commands.Cog, name="Miscellaneous"):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @commands.command(aliases=["add"])
    async def invite(self, ctx):
        """Provied the link to invite the bot to your server"""
        embed = discord.Embed(
            description=f"**[Click here to add {self.bot.user.name} to your Discord server](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot)**",
            color=0x00FF00,
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["upvote"])
    async def vote(self, ctx):
        """Vote for this discord bot so that other people can find it"""
        embed = discord.Embed(color=0x00FF00)
        embed.add_field(
            name="Vote:",
            value="Discord Bot List: **[VOTE HERE](https://top.gg/bot/691589447074054224)**\nBots For Discord: **[VOTE HERE](https://botsfordiscord.com/bot/691589447074054224)**",
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Check ping of client, message and api"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="Bot's Ping", color=0x00FF00)
        embed.add_field(name="API Ping", value=f"`{latency}ms`")

        await ctx.send(embed=embed)

    @commands.command(aliases=["statistics", "botinfo", "botinformation"])
    async def stats(self, ctx):
        """View statistics about the bot"""

        current_time = time.time()
        difference = int(round(current_time - self.bot.start_time))
        text = str(datetime.timedelta(seconds=difference))

        total_users = sum(len(guild.members) for guild in self.bot.guilds)
        text_channels = sum(len(guild.text_channels) for guild in self.bot.guilds)
        voice_channels = sum(len(guild.voice_channels) for guild in self.bot.guilds)

        ram = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (2 ** 20), 2)

        statics = ""
        statics += f"Guilds: `{len(self.bot.guilds):,}`\n"
        statics += f"Users: `{total_users:,}`\n"
        statics += f"Channels: `{text_channels+voice_channels:,}`\n"
        statics += f"Memory Usage: `{ram:,}MB`\n"
        statics += f"Uptime: `{text}`\n"
        statics += f"Discord.py: `v{discord.__version__}`"

        links = ""
        links += "[INVITE BOT](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot&permissions=314448)\n"
        links += "[GITHUB](https://github.com/Darkflame72/Obsidion)\n"
        links += "[SUPPORT SERVER](https://discord.gg/invite/7BRD7s6)\n"
        links += "[VOTE](https://top.gg/bot/691589447074054224)\n"
        links += "[TRELLO](https://trello.com/b/qZhxHkTq/obsidion)"

        embed = discord.Embed(title="Stats", color=0x00FF00)
        embed.add_field(name=":newspaper: STATS", value=statics, inline=True)
        embed.add_field(name=":link: LINKS", value=links, inline=True)
        embed.set_footer(text="Version: 0.1 | Authors: Darkflame72#1150")

        await ctx.send(embed=embed)

    @commands.command(aliases=["info", "commands", "obsidion"])
    async def help(self, ctx, *cog_name):
        """Gets all cogs and commands of mine."""
        if cog_name:
            if len(cog_name) > 1:
                await ctx.send(
                    f"{ctx.message.author.mention}, :x: Please enter only one command for help"
                )
            else:
                # get information on 1 cog
                cog_name = cog_name[0]
                found = False
                for x in self.bot.cogs:
                    for y in self.bot.get_cog(x).get_commands():
                        if y.name == cog_name:
                            embed = discord.Embed(
                                title=cog_name, description=y.help, color=0x00FF00
                            )
                            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
                            await ctx.author.send(embed=embed)
                            found = True
                            break
                if not found:
                    await ctx.send(
                        f"{ctx.message.author.mention}, :x: That command is not found please try again"
                    )
        else:
            prefixes = await self.bot.get_guild_prefixes(ctx.guild)
            del prefixes[1]
            embed = discord.Embed(
                description=f"Below is a list of commands you can use\n To use commands type `{prefixes[1]}command` or {prefixes[0]} command \n To get more information about a command type: `{prefixes[1]}help command`",
                color=0x00FF00,
            )
            embed.set_author(name="Bot's Commands")
            # General help command
            for cog in self.bot.cogs:
                cogs = []
                cog_commands = self.bot.get_cog(cog).get_commands()
                for c in cog_commands:
                    if not c.hidden:
                        cogs.append(c.name)
                if len(cogs) > 0:
                    embed.add_field(
                        name=cog, value=f"`{'`, `'.join(cogs)}`", inline=False
                    )
            embed.set_footer(text="Version: 0.1 | Authors: Darkflame72#1150")
            await ctx.send(embed=embed)

    @commands.command(aliases=["alias", "a", "aliaslist"])
    async def aliases(self, ctx):
        """Lists all the aliases you can use."""
        prefixes = await self.bot.get_guild_prefixes(ctx.guild)
        del prefixes[1]
        embed = discord.Embed(
            description=f"Below is a list of command aliases you can use\n To use aliases type `{prefixes[1]}alias` or {prefixes[0]} alias \n To get more information about a command type: `{prefixes[1]}help command`",
            color=0x00FF00,
        )
        embed.set_author(name="Bot's Commands")
        # General help command
        for cog in self.bot.cogs:
            cogs = []
            cog_commands = self.bot.get_cog(cog).get_commands()
            for c in cog_commands:
                if not c.hidden and len(c.aliases) >= 1:
                    cogs.append(f"**{c.name}**: `{', '.join(c.aliases)}`\n")
            if len(cogs) >= 1:
                embed.add_field(name=cog, value=f"{''.join(cogs)}", inline=False)
        embed.set_footer(text="Version: 0.1 | Authors: Darkflame72#1150")
        await ctx.send(embed=embed)

    @commands.command(aliases=["team", "staff", "developers"])
    async def credits(self, ctx):
        """See the team behind Obsidion and what services we use to bring you what you want"""
        embed = discord.Embed(title=f"{self.bot.user.name} Bot Credits", color=0x00FF00)
        embed.add_field(
            name="Developers",
            value="[Darkflame72#1150](https://github.com/Darkflame72/)",
        )
        # embed.add_field(name="Staff", value="")
        embed.add_field(
            name="Beta Testers",
            value="[Abhishek Rameshand#8069](https://www.youtube.com/channel/UC0L0CPqIoZzKeV7ndIXjZZw), [Arrow_Plays#8625](https://github.com/AjayACST/)",
        )
        embed.add_field(
            name="Contribute",
            value="[Contribute on Github](https://github.com/Darkflame72/Obsidion/)\n[Track the bots progress on Trello](https://trello.com/b/qZhxHkTq/obsidion)",
        )
        third_party = ""
        third_party += "This bot uses some external services to add extra features.\n"
        third_party += (
            "Skin renders - [Visage](https://visage.surgeplay.com/index.html)\n"
        )
        third_party += "Mojang API - [Wiki.vg](https://wiki.vg/Mojang_API)\n"
        third_party += (
            "Discord.py - [discord.py Github](https://github.com/Rapptz/discord.py)"
        )
        embed.add_field(name="Third Party Stuff", value=third_party, inline=False)

        embed.set_footer(text="Version: 0.1 | Authors: Darkflame72#1150")
        await ctx.send(embed=embed)
