from discord.ext import commands
import discord
import asyncio
from utils.db import Data
import resource
import config

class admin(commands.Cog, name="admin"):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(hidden=True)
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"The cog {module} has been succesfully loaded")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"The cog {module} has been succesfully unloaded")

    @commands.is_owner()
    @commands.group(name="reload", hidden=True, invoke_without_command=True)
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.reload_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"The cog {module} has been succesfully reloaded")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        users = sum([1 for m in guild.members if not m.bot])
        bots = sum([1 for m in guild.members if m.bot])
        members = f"Humans: `{users}/{len(guild.members)}` \n Bots: `{bots}/{len(guild.members)}`"
        
        if str(guild.id) in self.bot.pool["guilds"]:
            embed = discord.Embed(name=f"{self.bot.user.name} has re-joined a guild")
            embed.set_footer(text=f"Guild: {len(self.bot.guilds):,} | Shard: {guild.shard_id}/{self.bot.shard_count-1} | rejoin")
        else:
            embed = discord.Embed(name=f"{self.bot.user.name} has joined a new guild")
            embed.set_footer(text=f"Guild: {len(self.bot.guilds):,} | Shard: {guild.shard_id}/{self.bot.shard_count-1} | join")
            self.bot.pool["guilds"][guild.id] = {"prefix": "/", "server": None}
            Data.save("", self.bot.pool)
        embed.add_field(name="Name", value=f"`{guild.name}`")
        embed.add_field(name="Members", value=members)
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Region", value=guild.region, inline=False)
        if guild.icon_url:
            embed.set_thumbnail(url=guild.icon_url)
        else:
            embed.set_thumbnail(url="https://i.imgur.com/AFABgjD.png")
        channel = self.bot.get_channel(config.new_guild_channel)
        await channel.send(embed=embed)

    @commands.command(hidden=True)
    async def shardinfo(self, ctx):
        """Get info about the shards"""
        total_guilds = len(self.bot.guilds)
        total_users = sum(len(guild.members) for guild in self.bot.guilds)
        total_memory = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (2**20), 2)

        description = f"Total Guilds `{total_guilds:,}` | Total Users: `{total_users:,}` | Total Memory: `{total_memory:,} mb`"

        embed = discord.Embed(title="Shard info", color=0x00ff00, description=description)

        info = {}
        for i in range(self.bot.shard_count):
            value = ""
            value += "Status: :online:\n"
            value += f"Guilds: {sum(1 for guild in self.bot.guilds if guild.shard_id == i)}\n"
            value += f"Users: {sum(guild.member_count for guild in self.bot.guilds if guild.shard_id == i)}\n"
            value += f"Channels: {sum((len(guild.voice_channels) + len(guild.text_channels)) for guild in self.bot.guilds if guild.shard_id == i)}\n"
            value += f"Ping: {round(self.bot.latencies[i][1]*1000)} ms \n"
            embed.add_field(name=f"Shard: {i}", value=value)

        await ctx.send(embed=embed)