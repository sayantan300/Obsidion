from discord.ext import commands
import discord
import asyncio
import resource
import config
import os, sys
import traceback
from utils.utils import get


class admin(commands.Cog, name="admin"):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == self.bot.owner_id

    @commands.command(hidden=True)
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: {e.__class__.__name__}: {e}"
            )
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, :white_check_mark: The cog {module} has been succesfully loaded"
            )

    @commands.command(hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: {e.__class__.__name__}: {e}"
            )
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, :white_check_mark: The cog {module} has been succesfully unloaded"
            )

    @commands.group(name="reload", hidden=True, invoke_without_command=True)
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.reload_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: {e.__class__.__name__}: {e}"
            )
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, :white_check_mark: The cog {module} has been succesfully reloaded"
            )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if config.new_guild_channel:
            users = sum([1 for m in guild.members if not m.bot])
            bots = sum([1 for m in guild.members if m.bot])
            members = f"Humans: `{users}/{len(guild.members)}` \n Bots: `{bots}/{len(guild.members)}`"

            if await self.pool.fetch("SELECT * FROM guild WHERE id = $1", guild.id):
                embed = discord.Embed(
                    name=f"{self.bot.user.name} has re-joined a guild"
                )
                embed.set_footer(
                    text=f"Guild: {len(self.bot.guilds):,} | Shard: {guild.shard_id}/{self.bot.shard_count-1} | rejoin"
                )
            else:
                embed = discord.Embed(
                    name=f"{self.bot.user.name} has joined a new guild"
                )
                embed.set_footer(
                    text=f"Guild: {len(self.bot.guilds):,} | Shard: {guild.shard_id}/{self.bot.shard_count-1} | join"
                )
                self.bot.pool.execute(
                    "INSERT INTO guild (id, prefix, serverTrack, member_join, silent) VALUES ($1, $2, $3, $4, $5)",
                    guild.id,
                    "/",
                    None,
                    None,
                    False,
                )
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
        total_memory = round(
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (2 ** 20), 2
        )

        description = f"Total Guilds `{total_guilds:,}` | Total Users: `{total_users:,}` | Total Memory: `{total_memory:,} mb`"

        embed = discord.Embed(
            title="Shard info", color=0x00FF00, description=description
        )

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

    @commands.command(hidden=True)
    async def reboot(self, ctx):
        await ctx.send("Rebooting")
        os.execl(sys.executable, sys.executable, *sys.argv)

    @commands.command(hidden=True)
    async def shutdown(self, ctx):
        await ctx.send("Shutting Down")
        await ctx.bot.logout()


# Handles automatic posting
import dbl
import aiohttp


class bot_advertise(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vote_channel = config.upvote_channel
        if config.bots4discordToken:
            self.bfdtoken = config.bots4discordToken
            self.bg_task = bot.loop.create_task(self.loop_server_count())
        if config.dblToken:
            self.dbltoken = config.dblToken
            self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    async def loop_server_count(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            url = f"https://botsfordiscord.com/api/bot/{self.bot.user.id}"
            headers = {"Authorization": self.bfdtoken}
            json = {"server_count": len(self.bot.guilds)}
            async with aiohttp.ClientSession(headers=headers) as session:
                await session.post(url, json=json)
            await asyncio.sleep(600)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        embed = discord.Embed(
            title=f"New upvote for {self.bot.user.name} on top.gg",
            description=f"<@{data['user']}> Has just upvoted {self.bot.user.name}!",
        )
        channel = self.bot.get_channel(self.vote_channel)
        await channel.send(embed=embed)
