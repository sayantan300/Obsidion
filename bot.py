import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import datetime
import json
import logging
import traceback
import aiohttp
import sys
import asyncpg

log = logging.getLogger(__name__)


def token():
    # load token from json file
    with open("config.json", "r") as f:
        setup = json.load(f)
    return setup["setup"]["token"]


def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ']

    if msg.guild is None:
        base.append('/')
    else:
        with open("data.json", "r+") as f:
            json_data = json.load(f)
        prefix = json_data["server"][str(msg.guild.id)]
        base.append(prefix)
    return base


def extensions():
    with open("config.json", "r") as f:
        json_data = json.load(f)
    cogs = json_data["setup"]["cogs"]
    return cogs


class MinecraftDiscord(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, case_insensitive=True, help_command=None)

        self.session = aiohttp.ClientSession(loop=self.loop)

        for extension in extensions():
            try:
                self.load_extension(f"cogs.{extension}")
            except Exception as e:
                print(
                    f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}',
                      file=sys.stderr)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)

    def get_guild_prefixes(self, guild, *, local_inject=_prefix_callable):
        proxy_msg = discord.Object(id=None)
        proxy_msg.guild = guild
        return local_inject(self, proxy_msg)

    def get_raw_guild_prefixes(self, guild_id):
        return self.prefixes.get(guild_id, ['?', '!'])

    async def set_guild_prefixes(self, guild, prefixes):
        if len(prefixes) == 0:
            await self.prefixes.put(guild.id, [])
        elif len(prefixes) > 1:
            raise RuntimeError('Cannot have more than 1 custom prefixes.')
        else:
            await self.prefixes.put(guild.id, sorted(set(prefixes), reverse=True))

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        print(f"\n\nSuccessfully logged in and booted...!")
        print(f'Ready: {self.user} (ID: {self.user.id})')
        print(f"Version: {discord.__version__}\n")

        # Sets our bots status to wether operational or testing
        activity = discord.Activity(name=f"For @{self.user.name} help", type=discord.ActivityType.watching)
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_resumed(self):
        print('resumed...')

    async def on_guild_join(self, guild):
        if guild.id in self.blacklist:
            await guild.leave()

    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        super().run(token(), reconnect=True)
