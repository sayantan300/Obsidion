from discord.ext import commands
from random import choice
import discord
import resource
import aiohttp
import datetime
import time
import logging
import config
import itertools
import asyncio

log = logging.getLogger(__name__)


class Miscellaneous(commands.Cog, name="Miscellaneous"):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self
        self.bot = bot
        self.session = bot.session

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command(aliases=["add"])
    async def invite(self, ctx):
        """Invite the bot to your Discord server"""
        embed = discord.Embed(
            description=f"**[Click here to add {self.bot.user.name} to your Discord server](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot&permissions=314432)**",
            color=0x00FF00,
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["upvote"])
    async def vote(self, ctx):
        """Help support this bot by helping others to find it"""
        embed = discord.Embed(color=0x00FF00)
        embed.add_field(
            name="Vote:",
            value="""
            Discord Bot List: **[VOTE HERE](https://top.gg/bot/691589447074054224)**
            Bots For Discord: **[VOTE HERE](https://botsfordiscord.com/bot/691589447074054224)**
            Discord Boats List: **[VOTE HERE](https://discord.boats/bot/691589447074054224)**
            Bots On Discord: **[REVIEW HERE](https://bots.ondiscord.xyz/bots/691589447074054224/review)**
            """,
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
        embed.add_field(
            inline=False,
            name="Support",
            value="**[ADD TO SERVER](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot&permissions=314448) | [SUPPORT SERVER](https://discord.gg/invite/7BRD7s6)**",
        )
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
            value="[Contribute on Github](https://github.com/Darkflame72/Obsidion/)\n[Track on Trello](https://trello.com/b/qZhxHkTq/obsidion)",
        )

        embed.add_field(
            name="Inspiration",
            value="[Crafty](https://www.craftybot.xyz/) by [TJ#0215](https://github.com/talle117)",
        )
        third_party = ""
        third_party += "This bot uses some external services to add extra features.\n"
        third_party += (
            "Skin renders - [Visage](https://visage.surgeplay.com/index.html)\n"
        )
        third_party += "Mojang API - [Wiki.vg](https://wiki.vg/Mojang_API)\n"
        third_party += "Discord.py - [Github](https://github.com/Rapptz/discord.py)"
        embed.add_field(name="Third Party Stuff", value=third_party, inline=False)

        embed.set_footer(text="Version: 0.1 | Authors: Darkflame72#1150")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def feedback(self, ctx, *, content: str):
        """Gives feedback about the bot.
        This is a quick way to request features or bug fixes
        without being in the bot's server.
        The bot will communicate with you via PM about the status
        of your request if possible.
        You can only request feedback once a minute.
        """

        e = discord.Embed(title="Feedback", colour=0x00FF00)
        channel = self.bot.get_channel(config.feedback_channel)
        if channel is None:
            return

        e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        e.description = content
        e.timestamp = ctx.message.created_at

        if ctx.guild is not None:
            e.add_field(
                name="Server",
                value=f"{ctx.guild.name} (ID: {ctx.guild.id})",
                inline=False,
            )

        e.add_field(
            name="Channel", value=f"{ctx.channel} (ID: {ctx.channel.id})", inline=False
        )
        e.set_footer(text=f"Author ID: {ctx.author.id}")

        await channel.send(embed=e)
        await ctx.send("Successfully sent feedback")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def pm(self, ctx, user_id: int, *, content: str):
        user = self.bot.get_user(user_id)

        fmt = (
            content
            + "\n\n*This is a DM sent because you had previously requested feedback or I found a bug"
            " in a command you used, I do not monitor this DM.*"
        )
        try:
            await user.send(fmt)
        except:
            await ctx.send(f"Could not PM user by ID {user_id}.")
        else:
            await ctx.send("PM successfully sent.")


class MyHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={"help": "Shows help about the bot, a command, or a category"}
        )

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"[{command.name}|{aliases}]"
            if parent:
                fmt = f"{parent} {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{alias} {command.signature}"

    async def send_bot_help(self, mapping):
        bot = self.context.bot
        embed = discord.Embed(
            title="Bot support",
            description=f"Below is a list of commands you can use\nTo use commands type `{self.context.prefix}command` or <@{bot.user.id}> `command`\nTo get more information about a command type: `{self.context.prefix}help command`",
            colour=0x00FF00,
        )
        embed.set_footer(
            text=f'Use "{self.context.prefix}help command" for more info on a command.'
        )

        for cog in bot.cogs:
            cogs = []
            cog_commands = bot.get_cog(cog).get_commands()
            cogs = [c.name for c in cog_commands if not c.hidden]

            if len(cogs) > 0:
                embed.add_field(name=cog, value=f"`{'`, `'.join(cogs)}`", inline=False)

        embed.add_field(
            inline=False,
            name="Support",
            value=f"**[ADD TO SERVER](https://discordapp.com/oauth2/authorize?client_id={self.context.bot.user.id}&scope=bot&permissions=314448) | [SUPPORT SERVER](https://discord.gg/invite/7BRD7s6)** | **[GITHUB](https://github.com/Darkflame72/Obsidion/)**",
        )
        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        # I really don't want to do this
        pass

    def common_command_formatting(self, page_or_embed, command):
        page_or_embed.title = self.get_command_signature(command)
        if command.description:
            page_or_embed.description = f"{command.description}\n\n{command.help}"
        else:
            page_or_embed.description = command.help or "No help found..."

    async def send_command_help(self, command):
        embed = discord.Embed(colour=0x00FF00)

        self.common_command_formatting(embed, command)
        if len(command.aliases) > 0:
            embed.add_field(
                name=command.name,
                value=f"""
            Name: `{command.name}`
            Aliases: `{', '.join(command.aliases)}`
            Category: `{command.cog_name}`""",
            )
        else:
            embed.add_field(
                name=command.name,
                value=f"""
            Name: `{command.name}`
            Category: `{command.cog_name}`""",
            )
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(colour=0x00FF00)

        self.common_command_formatting(embed, group)

        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)

        sub = ""
        for entry in entries:
            sub += f"`{self.context.prefix}{group.name} {entry.name}` {entry.help}.\n"
        embed.add_field(name="Sub Commands:", value=sub)

        embed.add_field(
            name="Usage",
            value=f"`{self.context.prefix}{self.get_command_signature(group)}`",
            inline=False,
        )
        if len(group.aliases) > 0:
            embed.add_field(
                name=group.name,
                value=f"""
            Name: `{group.name}`
            Aliases: `{', '.join(group.aliases)}`
            Category: `{group.cog_name}`""",
            )
        else:
            embed.add_field(
                name=group.name,
                value=f"""
            Name: `{group.name}`
            Category: `{group.cog_name}`""",
            )

        await self.context.send(embed=embed)
