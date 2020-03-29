import discord
from discord.ext import commands
import aiohttp
import datetime

hypixel_api = "ecdcbe5e-3d63-4a90-a374-87bc5a9357f7"

async def get(session, url):
    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data
        else:
            return False

async def get_uuid(session, username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.json()
            uuid = data["id"]
            return uuid
        else:
            return False

class servers(commands.Cog, name="Servers"):

    def __init__(self, bot):
        self.session = bot.session

    #@commands.command()
    #async def blocksmcself(self, ctx, username):
    #    pass

    #@commands.command()
    #async def funcraft(self, ctx, username):
    #    pass

    #async def hivemc(self, ctx, username):
    #    pass

    @commands.command()
    async def hypixel(self, ctx, username):
        """Get information about a Hypixel user"""
        uuid = await get_uuid(self.session, username)
        if uuid:
            url = f"https://api.hypixel.net/player?key={hypixel_api}&uuid={uuid}"
            data = await get(self.session, url)
            embed = discord.Embed(color=0x00ff00)

            player=data["player"]

            information = ""
            information += f"Karma: `{player['karma']}`\n"
            information += f"Experience: `{player['networkExp']:,}`\n"
            information += f"Votes: `{player['voting']['total']}`\n"
            if "achievements" in player:
                information += f"Achievements: `{len(player['achievements'])}`\n"
            information += f"Completed Parkour: `{len(player['parkourCompletions'])}`\n"
            information += f"Version: `{player['mcVersionRp']}`\n"
            information += f"Last Games: `{player['mostRecentGameType']}`\n"

            dates = ""
            dates += f"First Logon: `{datetime.datetime.fromtimestamp(player['firstLogin'] / 1e3).strftime('%b %d, %Y')}`\n"
            dates += f"Last Login: `{datetime.datetime.fromtimestamp(player['lastLogin'] / 1e3).strftime('%b %d, %Y')}`\n"
            dates += f"Last Logout: `{datetime.datetime.fromtimestamp(player['lastLogout'] / 1e3).strftime('%b %d, %Y')}`\n"

            embed.add_field(name=":newspaper:INFORMATION", value=information)
            embed.add_field(name=":calendar:DATES", value=dates)

            await ctx.send(embed=embed)

    #@commands.command()
    #async def manacube(self, ctx, username):
    #    pass

    #@commands.command()
    #async def minesage(self, ctx, username):
    #    pass

    #@commands.command()
    #async def universocraft(self, ctx, username):
    #    pass

    #@commands.command()
    #async def veltpvp(self, ctx, username):
    #    pass

    #@commands.command()
    #async def wynncraft(self, ctx, username):
    #    uuid = get_uuid(self.session, username)
    #    if uuid:
    #        url = f"https://api.wynncraft.com/v2/player/{uuid}/stats"
    #        data = await get(self.session, url)

    #        embed = discord.Embed(color=0x00ff00)
    #        
    #        information = ""

    #        dates = ""
    #        dates += f"First Login: `{data['meta']['firstJoin']}`\n"
    #        dates += f"Last Login: `{data['meta']['lastJoin']}`"
    #        dates += f"Playtime: `{data['meta']['playtime']}`"

    #        await ctx.send(embed=embed)
    #    pass