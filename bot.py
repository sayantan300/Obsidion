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

import config

log = logging.getLogger(__name__)


def _prefix_callable(bot, msg):
    user_id = bot.user.id
    prefix = [f'<@!{user_id}> ', f'<@{user_id}> ']

    if msg.guild is None:
        prefix.append('/')
    else:
        prefix.append(bot.pool["guilds"][str(msg.guild.id)]["prefix"])
    return prefix


class MinecraftDiscord(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, case_insensitive=True,
                         help_command=None, owner_id=456217109236809748)

        self.client_id = config.client_id
        self.hypixel_api = config.hypixel_key
        self._prev_events = deque(maxlen=10)

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

    async def on_guild_join(self, guild):
        users = sum([1 for m in guild.members if not m.bot])
        bots = sum([1 for m in guild.members if m.bot])
        members = f"Humans: `{users}/{len(guild.members)}` \n Bots: `{bots}/{len(guild.members)}`"
        
        embed = discord.Embed(name=f"{self.user.name} has joined a new guild")
        embed.add_field(name="Name", value=f"`{guild.name}`")
        embed.add_field(name="Members", value=members)
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Region", value=guild.region, inline=False)
        if guild.icon_url:
            embed.set_thumbnail(url=guild.icon_url)
        else:
            embed.set_thumbnail(url="https://i.imgur.com/AFABgjD.png")
        if str(guild.id) in self.pool["guilds"]:
            embed.set_footer(text=f"Guild: {len(self.guilds):,} | Shard: {guild.shard_id}/{self.shard_count-1} | rejoin")
        else:
            embed.set_footer(text=f"Guild: {len(self.guilds):,} | Shard: {guild.shard_id}/{self.shard_count-1} | join")
            self.pool["guilds"][guild.id] = {"prefix": "/", "server": None}
            db.Data.save("", self.pool)
        channel = self.get_channel(694417026331967538)
        await channel.send(embed=embed)

    def run(self):
        super().run(config.token, reconnect=True)
