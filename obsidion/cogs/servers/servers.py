import discord
from discord.ext import commands
from .utils import *
from uuid import UUID
from obsidion.utils.utils import get_uuid


class servers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def check_username(ctx, username):
        try:
            val = UUID(username, version=4)
            return username
        except ValueError:
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            return get_uuid(ctx.bot.http_session, username)

    @commands.command()
    async def minesaga(self, ctx: commands.Context, username: str):
        """get stats from minesage"""
        await ctx.trigger_typing()
        data = await minesaga(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Minesaga or there are no stats"
            )
            return
        embed = discord.Embed(title=f"`{username}`'s Minesaga Stats", color=0x00FF00)
        embed.add_field(
            name="Online Stats",
            value=(
                f"Joined: `{data['joined']}`\nLast Seen: `{data['last_seen']}`\nPlay Time: `{data['play_time']}`"
            ),
        )
        embed.add_field(
            name="Island Stats",
            value=(
                f"Island: `{data['game_stats'][0]['Island']['Island']}`\nIsland Rank: `{data['game_stats'][0]['Island']['Island rank']}`\nIsland Position: `{data['game_stats'][0]['Island']['Island position']}`"
            ),
        )
        embed.add_field(
            name="General Stats",
            value=(
                f"Playtime: `{data['game_stats'][1]['General']['Playtime']}`\nBalance: `{data['game_stats'][1]['General']['Balance']}`\nCoinflips Won: `{data['game_stats'][1]['General']['Coinflips Won']}`\nJackpots Won: `{data['game_stats'][1]['General']['Jackpots Won']}`"
            ),
        )
        embed.add_field(
            name="Combat Stats",
            value=(
                f"Kills: `{data['game_stats'][2]['Combat']['Kills']}`\nDeaths: `{data['game_stats'][2]['Combat']['Deaths']}`\nKDR: `{data['game_stats'][2]['Combat']['KDR']}`\nBosses Killed: `{data['game_stats'][2]['Combat']['Bosses Killed']}`\nTotla Mob Kills: `{data['game_stats'][2]['Combat']['Total Mob Kills']}`"
            ),
        )

        await ctx.send(embed=embed)
    @commands.command()
    async def hiverank(self, ctx: commands.Context, username: str):
        """get stats from minesage"""
        await ctx.trigger_typing()
        data = await hiveMCRank(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Hive or there are no ranks available."
            )
            return
        embed = discord.Embed(title=f"`{username}`'s hive Rank", color=0x00FF00)
        embed.add_field(
            name="rank",
            value=(
                f"Rank: `{data['rank']}`"
            ),
        )
        await ctx.send(embed=embed)

