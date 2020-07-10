import discord
from discord.ext import commands
from .utils import *
from uuid import UUID
from obsidion.utils.utils import usernameToUUID


class servers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
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
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
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
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
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
        embed = discord.Embed(color=0x008CD3)
        embed.set_author(
            name=f"BlocksMC information for {username}",
            url=f"https://blocksmc.com/player/{username}",
            icon_url="https://blocksmc.com/templates3/src/logo-gray-sm.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
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
        embed = discord.Embed(color=0x82C228)
        embed.set_author(
            name=f"UniversoCraft information for {username}",
            url=f"https://www.universocraft.com/members/{username}",
            icon_url="https://www.universocraft.com/favicon.ico",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
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
        embed = discord.Embed(color=0x6696C2)
        embed.set_author(
            name=f"Minesaga information for {username}",
            url=f"https://www.minesaga.org/members/{username}",
            icon_url="https://www.minesaga.org/favicon.ico",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
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
    async def manacube(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await manacube(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Minesaga or their status is not available."
            )
            return
        embed = discord.Embed(color=0x11B7C4)
        embed.set_author(
            name=f"Manacube information for {username}",
            url=f"https://manacube.com/stats/player/{username}/",
            icon_url="https://manacube.com/styles/ndzn/manacube/img/logo-cube.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        embed.add_field(
            name=("Manacube Stats"),
            value=(
                f"Rank: `{data['rank']}`\nCubits: `{data['cubits']}`\nFirst Seen: `{data['firstSeen']}`\nLast Seen: `{data['lastSeenAgo']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Parkour Stats"),
            value=(
                f"Playtime: `{data['parkour']['playtime']}`\nMana: `{data['parkour']['mana']}`\nScore: `{data['parkour']['score']}`\nCourses: `{data['parkour']['courses']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Axtec Stats"),
            value=(
                f"Playtime: `{data['aztec']['playtime']}`\nMob Kills: `{data['aztec']['mobKills']}`\nMana: `{data['aztec']['mana']}`\nMoney: `{data['aztec']['money']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Oasis Stats"),
            value=(
                f"Playtime: `{data['oasis']['playtime']}`\nMob Kills: `{data['oasis']['mobKills']}`\nMana: `{data['oasis']['mana']}`\nMoney: `{data['oasis']['money']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Islands Stats"),
            value=(
                f"Playtime: `{data['islands']['playtime']}`\nMob Kills: `{data['islands']['mobKills']}`\nSilver: `{data['islands']['silver']}`\nMoney: `{data['islands']['money']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Survival Stats"),
            value=(
                f"Playtime: `{data['survival']['playtime']}`\nMob Kills: `{data['survival']['mobKills']}`\nMoney: `{data['survival']['money']}`\nQuests: `{data['survival']['quests']}`"
            ),
        )

        embed.add_field(
            name=("Manacube Aether Stats"),
            value=(
                f"Playtime: `{data['aether']['playtime']}`\nMining Level: `{data['aether']['miningLevel']}`\nMoney: `{data['aether']['money']}`\nRebirths: `{data['aether']['rebirths']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Atlas Stats"),
            value=(
                f"Playtime: `{data['atlas']['playtime']}`\nMining Level: `{data['atlas']['miningLevel']}`\nMoney: `{data['atlas']['money']}`\nRebirths: `{data['aether']['rebirths']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Creative Stats"),
            value=(
                f"Playtime: `{data['creative']['playtime']}`\nBlocks Placed: `{data['creative']['blocksplaced']}`\nBlocks Broken: `{data['creative']['blocksbroken']}`"
            ),
        )
        embed.add_field(
            name=("Manacube KitPvP Stats"),
            value=(
                f"Playtime: `{data['kitpvp']['playtime']}`\nLevel: `{data['kitpvp']['level']}`\nMoney: `{data['kitpvp']['money']}`\nKills: `{data['kitpvp']['kills']}`"
            ),
        )
        await ctx.send(embed=embed)

