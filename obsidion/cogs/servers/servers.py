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
    async def wyncraft(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await wyncraftClasses(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Wynncraft or their status is not available."
            )
            return
        len_data = len(data["classes"])
        embed = discord.Embed(color=0xA4EC66)
        embed.set_author(
            name=f"WynnCraft information for {username}",
            url=f"https://wynncraft.com/stats/player/{username}",
            icon_url="https://cdn.wynncraft.com/img/wynn.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await get_uuid(ctx.bot.http_session, username)}"
        )
        embed.timestamp = ctx.message.created_at
        for i in range(len_data):
            embed.add_field(
                name=data["classes"][i]["class_name"],
                value=(
                    f"Class Name: `{data['classes'][i]['class_name']}`\n"
                    f"Class Level: `{data['classes'][i]['class_level']}`\n"
                    f"Class Deaths: `{data['classes'][i]['class_deaths']}`"
                ),
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
        embed = discord.Embed(color=0xF1A90F)
        embed.set_author(
            name=f"GommeHD information for {username}",
            url=f"https://www.gommehd.net/player/index?playerName={username}",
            icon_url="https://www.gommehd.net/images/brandmark@3x.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await get_uuid(ctx.bot.http_session, username)}"
        )
        embed.timestamp = ctx.message.created_at
        for game in data["game_stats"]:
            value = ""
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
        embed = discord.Embed(color=0x2E39A7)
        embed.set_author(
            name=f"VeltPVP information for {username}",
            url=f"https://www.veltpvp.com/u/{username}",
            icon_url="https://www.veltpvp.com/resources/images/nav-logo.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await get_uuid(ctx.bot.http_session, username)}"
        )
        embed.timestamp = ctx.message.created_at
        embed.add_field(
            name=("VeltPVP Stats"),
            value=(
                f"Rank: `{data['rank']}`\nLast Seen: `{data['last_seen']}`\nCurrent Status: `{data['current_status']}`\nFirst Joined: `{data['first_joined']}`\nTime Played: `{data['time_played']}`"
            ),
        )
        embed.add_field(
            name=("VeltPVP HCF Stats"),
            value=(
                f"Kills: `{data['game_stats'][0]['HCF']['Kills']}`\nDeaths: `{data['game_stats'][0]['HCF']['Deaths']}`\nKDR: `{data['game_stats'][0]['HCF']['KDR']}`"
            ),
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def blocksmc(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await blocksmc(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto VeltPVP or their status is not available."
            )
            return
        embed = discord.Embed(color=0xF1A90F)
        embed.set_author(
            name=f"BlocksMC information for {username}",
            url=f"https://blocksmc.com/player/{username}",
            icon_url="https://blocksmc.com/templates3/src/logo-gray-sm.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await get_uuid(ctx.bot.http_session, username)}"
        )
        embed.timestamp = ctx.message.created_at
        for game in data["game_stats"]:
            value = ""
            name = list(game)
            name_new = name[0]
            scores = game[name_new]
            for key in scores.keys():
                value += f"{key}: {scores[key]}\n"
            embed.add_field(name=name_new, value=value)
        await ctx.send(embed=embed)

    @commands.command()
    async def universocraft(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await universocraft(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto VeltPVP or their status is not available."
            )
            return
        embed = discord.Embed(color=0xF1A90F)
        embed.set_author(
            name=f"UniversoCraft information for {username}",
            url=f"https://www.universocraft.com/members/{username}",
            icon_url="https://www.universocraft.com/favicon.ico",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await get_uuid(ctx.bot.http_session, username)}"
        )
        embed.timestamp = ctx.message.created_at
        for game in data["game_stats"]:
            value = ""
            name = list(game)
            name_new = name[0]
            scores = game[name_new]
            for key in scores.keys():
                value += f"{key}: {scores[key]}\n"
            embed.add_field(name=name_new, value=value)
        await ctx.send(embed=embed)

    @commands.command()
    async def minesaga(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await minesaga(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Minesaga or their status is not available."
            )
            return
        embed = discord.Embed(color=0xF1A90F)
        embed.set_author(
            name=f"Minesaga information for {username}",
            url=f"https://www.minesaga.org/members/{username}",
            icon_url="https://www.minesaga.org/favicon.ico",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await get_uuid(ctx.bot.http_session, username)}"
        )
        embed.timestamp = ctx.message.created_at
        for game in data["game_stats"]:
            value = ""
            name = list(game)
            name_new = name[0]
            scores = game[name_new]
            for key in scores.keys():
                value += f"{key}: {scores[key]}\n"
            embed.add_field(name=name_new, value=value)
        await ctx.send(embed=embed)

