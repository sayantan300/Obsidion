from discord.ext import commands
import discord

# required libraries
import datetime
import asyncio
import json
import logging
import traceback
import aiohttp
import sys
from collections import Counter, deque, defaultdict
import time
import pip
import os
import platform
import getpass
import contextlib

# import environment variables
import config

from core.global_checks import init_global_checks

# start logger
log = logging.getLogger(__name__)

__version__ = "0.2 BETA"


# custom prefix
async def _prefix_callable(bot, msg):
    user_id = bot.user.id
    prefix = [f"<@!{user_id}> ", f"<@{user_id}> "]

    # if in direct messages
    if msg.guild is None:
        prefix.append("/")
    else:
        # because the bot is still in BETA it is offline
        # a lot meaning that some guilds are not added so
        # this is a sanity check
        if await bot.pool.fetch("SELECT prefix FROM guild WHERE id = $1", msg.guild.id):
            guild_prefixes = await bot.pool.fetchval(
                "SELECT prefix FROM guild WHERE id = $1", msg.guild.id
            )
            prefix.append(guild_prefixes)
        else:
            # add the prefix to the database
            await bot.pool.execute(
                "INSERT INTO guild (id, prefix, serverTrack, server_join, silent) VALUES ($1, $2, $3, $4, $5)",
                msg.guild.id,
                "/",
                None,
                None,
                False,
            )
            prefix.append("/")
    return prefix


class Obsidion(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=_prefix_callable,
            case_insensitive=True,
            # help_command=None,
            owner_id=config.owner_id,
            fetch_offline_members=False,
        )

        # important tokens
        self.client_id = config.client_id
        self.hypixel_api = config.hypixel_key
        self._prev_events = deque(maxlen=10)
        self.start_time = time.time()

        # shard_id: List[datetime.datetime]
        # shows the last attempted IDENTIFYs and RESUMEs
        self.resumes = defaultdict(list)
        self.identifies = defaultdict(list)

        # aiohttp session for use throughout the bot
        self.session = aiohttp.ClientSession(loop=self.loop)

        # load all the cogs
        for cog in config.cogs:
            try:
                self.load_extension(f"cogs.{cog}")
            except Exception:
                print(f"Failed to load extension {cog}.", file=sys.stderr)
                traceback.print_exc()

        init_global_checks(self)

    def _clear_gateway_data(self):
        one_week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        for _, dates in self.identifies.items():
            to_remove = [index for index, dt in enumerate(dates) if dt < one_week_ago]
            for index in reversed(to_remove):
                del dates[index]

        for _, dates in self.resumes.items():
            to_remove = [index for index, dt in enumerate(dates) if dt < one_week_ago]
            for index in reversed(to_remove):
                del dates[index]

    async def on_socket_response(self, msg):
        self._prev_events.append(msg)

    async def before_identify_hook(self, shard_id, *, initial):
        self._clear_gateway_data()
        self.identifies[shard_id].append(datetime.datetime.utcnow())
        await super().before_identify_hook(shard_id, initial=initial)

    async def on_command_error(self, ctx, error):
        """
        The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        ignored = commands.CommandNotFound

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_perms
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)
            _message = f"I need the **{fmt}** permission(s) to run this command."
            await ctx.send(_message)
            return

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("This command has been disabled.")
            return

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(
                f"This command is on cooldown, please retry in {error.retry_after:.2f}s"
            )

        elif isinstance(error, commands.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_perms
            ]
            if len(missing) > 2:
                fmt = f'{"**, **".join(missing[:-1])}, and {missing[-1]}'
            else:
                fmt = " and ".join(missing)
            _message = f"You need the **{fmt}** permission(s) to use this command."
            await ctx.send(_message)
            return

        elif isinstance(error, commands.UserInputError):
            await ctx.send("Invalid input.")
            ctx.bot.help_command.context = ctx
            await ctx.bot.help_command.send_command_help(ctx.command)
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send("This command cannot be used in direct messages.")
            except discord.Forbidden:
                pass
            return

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
            return

        # for when that person tries to mess with your bot
        elif isinstance(error, commands.NotOwner):
            print(f"{ctx.message.author} attempted to run an {ctx.command}")
            return

        elif isinstance(error, asyncio.TimeoutError):
            await ctx.send(
                "You did not reply to the message, the command has been cancelled."
            )
            return

        # ignore all other exception types, but print them to stderr
        print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)

        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

    # make getting prefixes a bit nicer
    def get_guild_prefixes(self, guild, *, local_inject=_prefix_callable):
        proxy_msg = discord.Object(id=None)
        proxy_msg.guild = guild
        return local_inject(self, proxy_msg)

    async def on_message(self, message):
        # make sure our bot does not reply to other bots

        # process command
        await self.process_commands(message)

    async def process_commands(self, message):
        ctx = await self.get_context(message)

        if ctx.command is None:
            return

        # if ctx.command.name in self.pool["blacklist"][str(ctx.guild.id)]:
        #    if self.pool["blacklist"][str(ctx.guild.id)][ctx.command.name] == "All" or self.pool["blacklist"][str(ctx.guild.id)][ctx.command.name] == ctx.message.channel.id:
        #        if self.pool["guilds"][str(ctx.guild.id)]["silent"]:
        #            await ctx.send(f"{ctx.message.author.mention}, :x: The command {ctx.command.name} is blacklisted.")
        #            return
        await self.invoke(ctx)

    ##########################
    # Main Control Functions #
    ##########################

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = datetime.datetime.utcnow()

            info = (
                f"Debug Info for {self.user.name}\n\n"
                + f"{self.user.name} version: {__version__}\n"
                + "Successfully logged in and booted...!\n"
                + f"Ready: {self.user} (ID: {self.user.id})\n"
                + f"Logged in at: {self.uptime}"
            )

            print(info)

        # Sets our bots status to wether operational or testing
        activity = discord.Activity(
            name=f"For @{self.user.name} help", type=discord.ActivityType.watching
        )
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_shard_resumed(self, shard_id):
        print(f"Shard ID {shard_id} has resumed...")
        self.resumes[shard_id].append(datetime.datetime.utcnow())

    def run(self):
        try:
            super().run(config.token, reconnect=True)
        finally:
            # all the packdown controls
            with open("prev_events.log", "w", encoding="utf-8") as fp:
                for data in self._prev_events:
                    try:
                        x = json.dumps(data, ensure_ascii=True, indent=4)
                    except:
                        fp.write(f"{data}\n")
                    else:
                        fp.write(f"{x}\n")

    @property
    def config(self):
        return __import__("config")
