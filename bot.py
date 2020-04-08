from discord.ext import commands
import discord
from utils.db import Data

# required libraries
import datetime
import asyncio
import json
import logging
import traceback
import aiohttp
import sys
from collections import Counter, deque
import time

# import environment variables
import config

# start logger
log = logging.getLogger(__name__)


# custom prefix
def _prefix_callable(bot, msg):
    user_id = bot.user.id
    prefix = [f'<@!{user_id}> ', f'<@{user_id}> ']

    # if in direct messages
    if msg.guild is None:
        prefix.append('/')
    else:
        # because the bot is still in BETA it is offline
        # a lot meaning that some guilds are not added so
        # this is a sanity check
        if str(msg.guild.id) in bot.pool["guilds"]:
            prefix.append(bot.pool["guilds"][str(msg.guild.id)]["prefix"])
        else:
            # add the prefix to the database
            bot.pool["guilds"][str(msg.guild.id)] = {"prefix": "/", "server": None}
            Data.save("", bot.pool)
            return "/"
    
    return prefix


class Obsidion(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, case_insensitive=True,
                         help_command=None, owner_id=config.owner_id, fetch_offline_members=False)

        # important tokens
        self.client_id = config.client_id
        self.hypixel_api = config.hypixel_key
        self._prev_events = deque(maxlen=10)
        self.start_time = time.time()

        # aiohttp session for use throughout the bot
        self.session = aiohttp.ClientSession(loop=self.loop)

        # load all the cogs
        for cog in config.cogs:
            try:
                self.load_extension(f"cogs.{cog}")
            except Exception as e:
                print(f'Failed to load extension {cog}.', file=sys.stderr)
                traceback.print_exc()
    

    async def on_command_error(self, ctx, error):
        """
        The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)
        
        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = f'I need the **{fmt}** permission(s) to run this command.'
            await ctx.send(_message)
            return
        
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'This command has been disabled.')
            return

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f'This command is on cooldown, please retry in {error.retry_after:.2f}s')

        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = f'{"**, **".join(missing[:-1])}, and {missing[-1]}'
            else:
                fmt = ' and '.join(missing)
            _message = f'You need the **{fmt}** permission(s) to use this command.'
            await ctx.send(_message)
            return

        elif isinstance(error, commands.UserInputError):
            await ctx.send("Invalid input.")
            await self.send_command_help(ctx)
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send('This command cannot be used in direct messages.')
            except discord.Forbidden:
                pass
            return

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
            return

        # for when that person tries to mess with your bot
        elif isinstance(error, commands.NotOwner):
            print(f"{ctx.message.author} attempted to run an {ctx.command}")

        # ignore all other exception types, but print them to stderr
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)

        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    # make getting prefixes a bit nicer
    def get_guild_prefixes(self, guild, *, local_inject=_prefix_callable):
        proxy_msg = discord.Object(id=None)
        proxy_msg.guild = guild
        return local_inject(self, proxy_msg)

    async def on_message(self, message):
        # make sure our bot does not reply to other bots
        if message.author.bot:
            return

        # process command
        await self.process_commands(message)


    ##########################
    # Main Control Functions #
    ##########################
    
    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        print(f"\n\nSuccessfully logged in and booted...!")
        print(f'Ready: {self.user} (ID: {self.user.id})')
        print(f"Version: {discord.__version__}\n")

        # Sets our bots status to wether operational or testing
        activity = discord.Activity(
            name=f"For @{self.user.name} help", type=discord.ActivityType.watching)
        await self.change_presence(status=discord.Status.online, activity=activity)
    
    async def close(self):
        await super().close()
        await self.session.close()

    async def on_resumed(self):
        print('resumed...')
    
    def run(self):
        try:
            super().run(config.token, reconnect=True)
        finally:
            # all the packdown controls
            with open('prev_events.log', 'w', encoding='utf-8') as fp:
                for data in self._prev_events:
                    try:
                        x = json.dumps(data, ensure_ascii=True, indent=4)
                    except:
                        fp.write(f'{data}\n')
                    else:
                        fp.write(f'{x}\n')

    @property
    def config(self):
        return __import__('config')
