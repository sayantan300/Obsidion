import discord
from discord.ext import commands
from .utils import *
from uuid import UUID
from obsidion.utils.utils import get_uuid


class hivestats(commands.Cog):
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
    async def hiverank(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await hiveMCRank(username, ctx.bot.http_session)
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Hive or there are no ranks available."
            )
            return
        embed = discord.Embed(title=f"`{username}`'s Hive Rank", color=0xFFAF03)
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
        embed = discord.Embed(
            title=f"`{username}`'s current Hive Status", color=0xFFAF03
        )
        embed.add_field(
            name="description",
            value=(f"Description: `{data['status'][0]['description']}`"),
        )
        embed.add_field(name="game", value=(f"Game: `{data['status'][0]['game']}`"))
        await ctx.send(embed=embed)

    @commands.command()
    async def hiveach(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        data = await hiveMCAchievements(username, ctx.bot.http_session)

        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Hive or they have no achievements."
            )
            return
        embed = discord.Embed(title=f"`{username}`'s Hive achievements", color=0xFFAF03)
        embed.add_field(
            name="description", value=(f"Description: `{data['all_achievements'][0]}`"),
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def hivestats(self, ctx: commands.Context, username: str, game: str):
        await ctx.trigger_typing()
        if game.lower() == "survival_games":
            data = await hiveMCGameStats(username, "SG", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Survival Games.", color=0xFFAF03
            )
            embed.add_field(
                name="Survival Game Stats",
                value=(
                    f"Victories: `{data['stats'][0]['victories']}`\nTotal points: `{data['stats'][0]['total_points']}`\nTotal games played: `{data['stats'][0]['gamesplayed']}`\nTotal number of death matches: `{data['stats'][0]['deathmatches']}`\nTotal kills: `{data['stats'][0]['kills']}`\nTotal deaths: `{data['stats'][0]['deaths']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "blockparty":
            data = await hiveMCGameStats(username, "BP", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for BlockParty.", color=0xFFAF03
            )
            embed.add_field(
                name="BlockParty Stats",
                value=(
                    f"Total games played: `{data['stats'][0]['games_played']}`\nTotal eliminations: `{data['stats'][0]['total_eliminations']}`\nTotal placings: `{data['stats'][0]['total_placing']}`\nTotal points: `{data['stats'][0]['total_points']}`\nVictories: `{data['stats'][0]['victories']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "cowboys_and_indians":
            data = await hiveMCGameStats(username, "CAI", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Cowboys and Indians.",
                color=0xFFAF03,
            )
            embed.add_field(
                name="Cowboys And Indians Stats",
                value=(
                    f"Total points: `{data['stats'][0]['total_points']}`\nTimes captured: `{data['stats'][0]['captured']}`\nTotal captures: `{data['stats'][0]['captures']}`\nTotal catches: `{data['stats'][0]['catches']}`\nTimes caught: `{data['stats'][0]['caught']}`\nGames played: `{data['stats'][0]['gamesplayed']}`\nVictories: `{data['stats'][0]['victories']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "cranked":
            data = await hiveMCGameStats(username, "CR", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Cranked.", color=0xFFAF03
            )
            embed.add_field(
                name="Cranked Stats",
                value=(
                    f"Total points: `{data['stats'][0]['total_points']}`\nVictories: `{data['stats'][0]['victories']}`\nTotal kills: `{data['stats'][0]['kills']}`\nTotal deaths: `{data['stats'][0]['deaths']}`\nGames played: `{data['stats'][0]['gamesplayed']}`\nRccat count: `{data['stats'][0]['rccat_count']}`\nRccat kills: `{data['stats'][0]['rccat_kills']}`\nAirstrike count: `{data['stats'][0]['airstrike_count']}`\nAirstrike kills: `{data['stats'][0]['airstrike_kills']}`\nSonicsquid count: `{data['stats'][0]['sonicsquid_count']}`\nSonicsquid kills: `{data['stats'][0]['sonicsquid_kills']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "deathrun":
            data = await hiveMCGameStats(username, "DR", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for DeathRun.", color=0xFFAF03
            )
            embed.add_field(
                name="DeathRun Stats",
                value=(
                    f"Total points: `{data['stats'][0]['total_points']}`\nVictories: `{data['stats'][0]['victories']}`\nTotal kills: `{data['stats'][0]['kills']}`\nTotal deaths: `{data['stats'][0]['deaths']}`\nGames played: `{data['stats'][0]['games_played']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "the_herobrine":
            data = await hiveMCGameStats(username, "HB", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for The Herobrine.", color=0xFFAF03
            )
            embed.add_field(
                name="The Herobrine Stats",
                value=(
                    f"Total captures: `{data['stats'][0]['captures']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal deaths: `{data['stats'][0]['deaths']}`\nTotal points: `{data['stats'][0]['points']}`\nCurrent class: `{data['stats'][0]['active_class']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "sg:heros":
            data = await hiveMCGameStats(username, "HERO", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for SG:Heros.", color=0xFFAF03
            )
            embed.add_field(
                name="SG:Heros Stats",
                value=(
                    f"Total points: `{data['stats'][0]['total_points']}`\nVictories: `{data['stats'][0]['victories']}`\nTotal kills: `{data['stats'][0]['kills']}`\nTotal deaths: `{data['stats'][0]['deaths']}`\nCurrent One V One Wins: `{data['stats'][0]['one_vs_ones_wins']}`\nTotal Game Plays: `{data['stats'][0]['games_played']}`\nTotal Deathmatches: `{data['stats'][0]['deathmatches']}`\nTotal TNT Used: `{data['stats'][0]['tnt_used']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "hide_and_seek":
            data = await hiveMCGameStats(username, "HIDE", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Hide And Seek.", color=0xFFAF03
            )
            embed.add_field(
                name="Hide And Seek Stats",
                value=(
                    f"Total points: `{data['stats'][0]['total_points']}`\nVictories: `{data['stats'][0]['victories']}`\nTotal Hider Kills: `{data['stats'][0]['hiderkills']}`\nTotal Seeker Kills: `{data['stats'][0]['seekerkills']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "one_in_the_chamber":
            data = await hiveMCGameStats(username, "OITC", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for One in the chamber.",
                color=0xFFAF03,
            )
            embed.add_field(
                name="One in the chamberStats",
                value=(
                    f"Total points: `{data['stats'][0]['total_points']}`\nVictories: `{data['stats'][0]['victories']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Arrows Fired: `{data['stats'][0]['arrowsfired']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "splegg":
            data = await hiveMCGameStats(username, "SP", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Splegg.", color=0xFFAF03
            )
            embed.add_field(
                name="Splegg Stats",
                value=(
                    f"Total Victories: `{data['stats'][0]['victories']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`\nTotal Eggs Fired: `{data['stats'][0]['eggsfired']}`\nTotal Blocks Destroyed: `{data['stats'][0]['blocksdestroyed']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`\nTotal Points: `{data['stats'][0]['points']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "trouble_in_mineville":
            data = await hiveMCGameStats(username, "TIMV", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Splegg.", color=0xFFAF03
            )
            embed.add_field(
                name="Splegg Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nMost Points: `{data['stats'][0]['most_points']}`\nTotal Role Points: `{data['stats'][0]['role_points']}`\nTotal Traitor Points: `{data['stats'][0]['t_points']}`\nTotal Innocent Points: `{data['stats'][0]['i_points']}`\nTotal Detective Points: `{data['stats'][0]['d_points']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "skywars":
            data = await hiveMCGameStats(username, "SKY", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            await ctx.send(data)
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for SkyWars.", color=0xFFAF03
            )
            embed.add_field(
                name="SkyWars Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nMost Points: `{data['stats'][0]['most_points']}`\nTotal Role Points: `{data['stats'][0]['role_points']}`\nTotal Traitor Points: `{data['stats'][0]['t_points']}`\nTotal Innocent Points: `{data['stats'][0]['i_points']}`\nTotal Detective Points: `{data['stats'][0]['d_points']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "the_lab":
            data = await hiveMCGameStats(username, "LAB", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for The Lab.", color=0xFFAF03
            )
            embed.add_field(
                name="The Lab Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nVictories: `{data['stats'][0]['victories']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "draw_it":
            data = await hiveMCGameStats(username, "DRAW", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Draw It.", color=0xFFAF03
            )
            embed.add_field(
                name="Draw It Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nVictories: `{data['stats'][0]['victories']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`\nTotal Correct Guesses: `{data['stats'][0]['correct_guesses']}`\nTotal Incorrect Guesses: `{data['stats'][0]['incorrect_guesses']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "slaparoo":
            data = await hiveMCGameStats(username, "SLAP", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Slaparoo.", color=0xFFAF03
            )
            embed.add_field(
                name="Slaparoo Stats",
                value=(
                    f"Total Victories: `{data['stats'][0]['victories']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`\nTotal Points: `{data['stats'][0]['points']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "electric_floor":
            data = await hiveMCGameStats(username, "EF", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Electric Floor.", color=0xFFAF03
            )
            embed.add_field(
                name="Electric Floor Stats",
                value=(
                    f"Total Victories: `{data['stats'][0]['victories']}`\nTimes Outlived: `{data['stats'][0]['outlived']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`\nTotal Points: `{data['stats'][0]['points']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "music_masters":
            data = await hiveMCGameStats(username, "MM", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Music Masters.", color=0xFFAF03
            )
            embed.add_field(
                name="Music Masters Stats",
                value=(
                    f"Total Victories: `{data['stats'][0]['victories']}`\nTotal Correct Notes: `{data['stats'][0]['correctnotes']}`\nTotal Incorrect Notes: `{data['stats'][0]['incorrectnotes']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`\nTotal Points: `{data['stats'][0]['points']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`\nTotal Perfect Notes: `{data['stats'][0]['notes_perfect']}`\nTotal Good Notes: `{data['stats'][0]['notes_good']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "gravity":
            data = await hiveMCGameStats(username, "GRAV", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Gravity.", color=0xFFAF03
            )
            embed.add_field(
                name="Gravity Stats",
                value=(
                    f"Total Victories: `{data['stats'][0]['victories']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`\nTotal Points: `{data['stats'][0]['points']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "restaurant_rush":
            data = await hiveMCGameStats(username, "RR", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Restaurant Rush.", color=0xFFAF03
            )
            embed.add_field(
                name="Restaurant Rush Stats",
                value=(
                    f"Total Victories: `{data['stats'][0]['victories']}`\nTotal Tables Cleared: `{data['stats'][0]['tablescleared']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`\nHigh Score: `{data['stats'][0]['highscore']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "skygiants":
            data = await hiveMCGameStats(username, "GNT", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for SkyGiants.", color=0xFFAF03
            )
            embed.add_field(
                name="SkyGiants Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nTotal Victories: `{data['stats'][0]['victories']}`\nTotal Games Played: `{data['stats'][0]['games_played']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`\nGold Earned: `{data['stats'][0]['gold_earned']}`\nTotal Beasts Slain: `{data['stats'][0]['beasts_slain']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "skygiants:_mini":
            data = await hiveMCGameStats(username, "GNTM", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for SkyGiants: Mini.", color=0xFFAF03
            )
            embed.add_field(
                name="SkyGiants: Mini Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nTotal Victories: `{data['stats'][0]['victories']}`\nTotal Games Played: `{data['stats'][0]['games_played']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`\nGold Earned: `{data['stats'][0]['gold_earned']}`\nTotal Beasts Slain: `{data['stats'][0]['beasts_slain']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "pumpkinfection":
            data = await hiveMCGameStats(username, "PMK", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Pumpkinfection.", color=0xFFAF03
            )
            embed.add_field(
                name="Pumpkinfection Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nTotal Victories: `{data['stats'][0]['victories']}`\nTotal Infections: `{data['stats'][0]['infections']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Games Played: `{data['stats'][0]['games_played']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "survival_games_2":
            data = await hiveMCGameStats(username, "SGN", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            await ctx.send(data)
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Survival Games 2.", color=0xFFAF03
            )
            embed.add_field(
                name="Survival Games 2 Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nTotal Victories: `{data['stats'][0]['victories']}`\nTotal Infections: `{data['stats'][0]['infections']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Games Played: `{data['stats'][0]['games_played']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "batterydash":
            data = await hiveMCGameStats(username, "BD", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for BatteryDash.", color=0xFFAF03
            )
            embed.add_field(
                name="BatteryDash Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nTotal Games Played: `{data['stats'][0]['games_played']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`\nTotal Energy Collected: `{data['stats'][0]['energy_collected']}`\nTotal Batteries Charged: `{data['stats'][0]['batteries_charged']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "sploop":
            data = await hiveMCGameStats(username, "SPL", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Sploop.", color=0xFFAF03
            )
            embed.add_field(
                name="Sploop Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nTotal Victories: `{data['stats'][0]['victories']}`\nTotal Games Played: `{data['stats'][0]['games_played']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`\nTotal Amount of Blocks Painted: `{data['stats'][0]['blocks_painted']}`\nTotal Ultimates Earned: `{data['stats'][0]['ultimates_earned']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "murder_in_mineville":
            data = await hiveMCGameStats(username, "MIMV", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Murder In Mineville.", color=0xFFAF03
            )
            embed.add_field(
                name="Murder In Mineville Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nTotal Games Played: `{data['stats'][0]['games_played']}`\nTotal Victories: `{data['stats'][0]['victories']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "bedwars":
            data = await hiveMCGameStats(username, "BED", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for BedWars.", color=0xFFAF03
            )
            embed.add_field(
                name="BedWars Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nTotal Victories: `{data['stats'][0]['victories']}`\nTotal Games Played: `{data['stats'][0]['games_played']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`\nTotal Beds Destroyed: `{data['stats'][0]['beds_destroyed']}`\nTotal Teams Eliminated: `{data['stats'][0]['teams_eliminated']}`\nWin Streak: `{data['stats'][0]['win_streak']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "survive_the_night":
            data = await hiveMCGameStats(username, "SURV", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Survive The Night.", color=0xFFAF03
            )
            embed.add_field(
                name="Survive The Night Stats",
                value=(
                    f"Total Points: `{data['stats'][0]['total_points']}`\nTotal Victories: `{data['stats'][0]['victories']}`\nTotal Games Played: `{data['stats'][0]['games_played']}`\nTotal Kills: `{data['stats'][0]['kills']}`\nTotal Deaths: `{data['stats'][0]['deaths']}`\nTotal Generators Powered: `{data['stats'][0]['generators_powered']}`"
                ),
            )
            await ctx.send(embed=embed)
        elif game.lower() == "explosive_eggs":
            data = await hiveMCGameStats(username, "EE", ctx.bot.http_session)
            if not data:
                await ctx.send(
                    f"{username} has not logged onto Hive or they have no game stats"
                )
                return
            embed = discord.Embed(
                title=f"`{username}`'s Hive stats for Explosive Eggs.", color=0xFFAF03
            )
            embed.add_field(
                name="Explosive Eggs Stats",
                value=(
                    f"Total Victories: `{data['stats'][0]['victories']}`\nTotal Leaps: `{data['stats'][0]['leaps']}`\nTotal Games Played: `{data['stats'][0]['gamesplayed']}`\nTotal Points: `{data['stats'][0]['points']}`"
                ),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry that game was not recognized as a Hive game")
