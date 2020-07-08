from asyncpixel import Client

import discord
from discord.ext import commands

from obsidion import constants


class hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.http_session

        self.hypixel_session = Client(constants.Bot.hypixelapi_token)

    @commands.command()
    async def watchdogstats(self, ctx: commands.Context):
        """Get the current watchdog statistics."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_watchdog_stats()
        embed = discord.Embed(title="Watchdog Stats", colour=0x00FF00)
        embed.add_field(name="Total Bans", value=f"{data.watchdog_total:,}")
        embed.add_field(name="Rolling Daily", value=f"{data.watchdog_rollingDaily:,}")
        embed.add_field(name="Last Minute", value=f"{data.watchdog_lastMinute:,}")
        embed.add_field(name="Staff Total", value=f"{data.staff_total:,}")
        embed.add_field(
            name="Staff Rolling Daily", value=f"{data.staff_rollingDaily:,}"
        )
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command()
    async def boosters(self, ctx: commands.Context):
        """Get the current boosters online."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_boosters()
        # it is a tuple of a list of all the different boosters
        embed = discord.Embed(
            title="Boosters",
            description=f"Total Boosters online: {len(data.boosters):,}",
            colour=0x00FF00,
        )
        await ctx.send(embed=embed)

    # @commands.command()
    async def hypixel_friends(self, ctx: commands.Context, uuid: str):
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_player_friends(uuid)

        # TODO

    @commands.command()
    async def hypixel_online(self, ctx: commands.Context):
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_player_count()
        embed = discord.Embed(
            title="Amount of Player on Hypixel", description=data, colour=0x00FF00
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def hypixel_player_status(self, ctx: commands.Context, uuid: str):
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_player_status(uuid)
        embed = discord.Embed(title="Curret player status", colour=0x00FF00)
        embed.add_field(name="Online", value=data.online)
        if data.online:
            embed.add_field(name="Current Game", value=data.gameType)
            embed.add_field(name="Current Mode", value=data.mode)
            embed.add_field(name="Current Map", value=data.map)
        await ctx.send(embed=embed)

    @commands.command()
    async def hypixel_player(self, ctx: commands.Context, uuid: str):
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_player(uuid)
        # TODO
