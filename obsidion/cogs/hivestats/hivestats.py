import discord
from discord.ext import commands
from .utils import hiveMCGameStats, hiveMCStatus, hiveMCRank
from obsidion.utils.utils import get_uuid

hive_con = {
    # "survival_games": "SG",
    "blockparty": "BP",
    "cowboys_and_indians": "CAI",
    "cranked": "CR",
    "deathrun": "DR",
    "the_herobrine": "HB",
    "sg:heros": "HERO",
    "hide_and_seek": "HIDE",
    "one_in_the_chamber": "OITC",
    "splegg": "SP",
    "trouble_in_mineville": "TIMV",
    "skywars": "SKY",
    "the_lab": "LAB",
    "draw_it": "DRAW",
    "slaparoo": "SLAP",
    "electric_floor": "EF",
    "music_masters": "MM",
    "gravity": "GRAV",
    "restaurant_rush": "RR",
    "skygiants": "GNT",
    "skygiants:_mini": "GNTM",
    "pumpkinfection": "PMK",
    "survival_games_2": "SGN",
    "batterydash": "BD",
    "sploop": "SPL",
    "murder_in_mineville": "MIMV",
    "bedwars": "BED",
    "survive_the_night": "SURV",
    "explosive_eggs": "EE",
}


class hivestats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hiverank(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await hiveMCRank(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Hive or there are no ranks available."
            )
            return
        embed = discord.Embed(color=0xFFAF03)
        embed.set_author(
            name=f"Hive rank for {username}",
            url=f"https://www.hivemc.com/player/{username}",
            icon_url="https://www.hivemc.com/favicon.ico",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await get_uuid(ctx.bot.http_session, username)}"
        )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name="rank", value=(f"Rank: `{data['rank'][0]}`"))
        await ctx.send(embed=embed)

    @commands.command()
    async def hivestatus(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await hiveMCStatus(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Hive or their status is not available."
            )
            return
        embed = discord.Embed(color=0xFFAF03)
        embed.set_author(
            name=f"Hive Status for {username}",
            url=f"https://www.hivemc.com/player/{username}",
            icon_url="https://www.hivemc.com/favicon.ico",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await get_uuid(ctx.bot.http_session, username)}"
        )
        embed.timestamp = ctx.message.created_at
        embed.add_field(
            name="description",
            value=(f"Description: `{data['status'][0]['description']}`"),
        )
        embed.add_field(name="game", value=(f"Game: `{data['status'][0]['game']}`"))
        await ctx.send(embed=embed)

    @commands.command()
    async def hivestats(self, ctx: commands.Context, username: str, game: str):
        await ctx.trigger_typing()

        if game.lower() in hive_con:
            data = await hiveMCGameStats(
                username, hive_con[game.lower()], ctx.bot.http_session
            )
            embed = discord.Embed(color=0xFFAF03)
            embed.set_author(
                name=f"Hive Stats for {username}",
                url=f"https://www.hivemc.com/player/{username}",
                icon_url="https://www.hivemc.com/favicon.ico",
            )
            embed.set_thumbnail(
                url=f"https://visage.surgeplay.com/bust/{await get_uuid(ctx.bot.http_session, username)}"
            )
            embed.timestamp = ctx.message.created_at
            if not data:
                await ctx.send("No stats found")
            del data["stats"][0]["UUID"]
            if "cached" in data["stats"][0]:
                del data["stats"][0]["cached"]
            if "firstLogin" in data["stats"][0]:
                del data["stats"][0]["firstLogin"]
            if "lastLogin" in data["stats"][0]:
                del data["stats"][0]["lastLogin"]
            if "achievements" in data["stats"][0]:
                del data["stats"][0]["achievements"]
            if "title" in data["stats"][0]:
                del data["stats"][0]["title"]
            value = ""
            for stat in data["stats"][0]:
                if isinstance(data["stats"][0][stat], list) or isinstance(
                    data["stats"][0][stat], dict
                ):
                    pass
                value += f"`{stat}`: {data['stats'][0][stat]}\n"
            embed.add_field(
                name=f"{game.replace('_', ' ').upper()} Stats", value=value,
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry that game was not recognized as a Hive game")
