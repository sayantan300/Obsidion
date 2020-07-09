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
    async def wyncraft(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await wyncraftClasses(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Wynncraft or their status is not available."
            )
            return
        len_data = len(data['classes'])
        embed = discord.Embed(
            title=f"`{username}`'s Wynncraft Classes", color=0xA4EC66
        )
        for i in range(len_data):
            embed.add_field(
                name=data['classes'][i]['class_name'],
                value=(f"Class Name: `{data['classes'][i]['class_name']}`\nClass Level: `{data['classes'][i]['class_level']}`\nClass Deaths: `{data['classes'][i]['class_deaths']}`"),
            )
        await ctx.send(embed=embed)
    @commands.command()
    async def gommehd(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await gommehd(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto GommeHD or their status is not available."
            )
            return
        embed = discord.Embed(
            title=f"`{username}`'s GommeHD Games", color=0xF1A90F
        )
        for game in data["game_stats"]:
            value=""
            name = list(game)
            name_new = name[0]
            scores = game[name_new]
            for key in scores.keys():
                value += f"{key}: {scores[key]}\n"
            embed.add_field(name=name_new, value=value)
        await ctx.send(embed=embed)
    @commands.command()
    async def veltpvp(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await veltpvp(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto VeltPVP or their status is not available."
            )
            return
        embed = discord.Embed(
            title=f"`{username}`'s VeltPVP Stats", color=0x2E39A7
        )
        embed.add_field(
            name=("VeltPVP Stats"),
            value=(f"Rank: `{data['rank']}`\nLast Seen: `{data['last_seen']}`\nCurrent Status: `{data['current_status']}`\nFirst Joined: `{data['first_joined']}`\nTime Played: `{data['time_played']}`"),
        )
        embed.add_field(
            name=("VeltPVP HCF Stats"),
            value=(f"Kills: `{data['game_stats'][0]['HCF']['Kills']}`\nDeaths: `{data['game_stats'][0]['HCF']['Deaths']}`\nKDR: `{data['game_stats'][0]['HCF']['KDR']}`"),
        )
        await ctx.send(embed=embed)

