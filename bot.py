from discord.ext import commands
import discord
from utils import db

import datetime
import re
import json
import asyncio
import copy
import logging
import traceback
import aiohttp
import sys
from collections import Counter, deque
import time

import config

log = logging.getLogger(__name__)


def _prefix_callable(bot, msg):
    user_id = bot.user.id
    prefix = [f'<@!{user_id}> ', f'<@{user_id}> ']

    if msg.guild is None:
        prefix.append('/')
    else:
        if str(msg.guild.id) in bot.pool["guilds"]:
            prefix.append(bot.pool["guilds"][str(msg.guild.id)]["prefix"])
        else:
            bot.pool["guilds"][str(msg.guild.id)] = {"prefix": "/", "server": None}
            db.Data.save("", bot.pool)
            return "/"
    return prefix


class Osisdion(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, case_insensitive=True,
                         help_command=None, owner_id=456217109236809748)

        self.client_id = config.client_id
        self.hypixel_api = config.hypixel_key
        self._prev_events = deque(maxlen=10)
        self.start_time = time.time()


        self.session = aiohttp.ClientSession(loop=self.loop)

        for cog in config.cogs:
            try:
                self.load_extension(f"cogs.{cog}")
            except Exception as e:
                print(f'Failed to load extension {cog}.', file=sys.stderr)
                traceback.print_exc()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{ctx.message.author.mention}, :x: This command is ratelimited, please try again in {error.retry_after:.2f}s')
        elif isinstance(error, commands.NotOwner):
            print(f"{ctx.message.author} attempted to run an {ctx.command}")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.BotMissingPermissions):
            print(error.missing_perms)
            await ctx.send(f"{ctx.message.author.mention}, :x: Unfortuantly the bot does not have the required permissions to excecute this command")
        #elif isinstance(error, commands.MissingRequiredArgument):
            #await ctx.send(f"{ctx.message.author.mention}, :x: The command was missing {error.param}")
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}',
                      file=sys.stderr)

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

    async def on_resumed(self):
        print('resumed...')

    async def close(self):
        await super().close()
        await self.session.close()

    @property
    def config(self):
        return __import__('config')

    async def on_socket_response(self, msg):
        self._prev_events.append(msg)

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)


    def run(self):
        try:
            super().run(config.token, reconnect=True)
        finally:
            with open('prev_events.log', 'w', encoding='utf-8') as fp:
                for data in self._prev_events:
                    try:
                        x = json.dumps(data, ensure_ascii=True, indent=4)
                    except:
                        fp.write(f'{data}\n')
                    else:
                        fp.write(f'{x}\n')
