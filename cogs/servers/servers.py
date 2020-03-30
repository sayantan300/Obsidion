import discord
from discord.ext import commands
import aiohttp
import datetime
import asyncio

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
        self.bot = bot

    #@commands.command()
    #async def blocksmcself(self, ctx, username):
    #    pass

    #@commands.command()
    #async def funcraft(self, ctx, username):
    #    pass

    #async def hivemc(self, ctx, username):
    #    pass
'''
    @commands.command()
    async def hypixel(self, ctx, username):
        """Get information about a Hypixel user"""
        uuid = await get_uuid(self.session, username)
        if uuid:
            url = f"https://api.hypixel.net/player?key={hypixel_api}&uuid={uuid}"
            data = await get(self.session, url)
            embed = discord.Embed(title=f"Hypixel player profile for {username}", color=0x00ff00)

            player=data["player"]

            information = ""
            information += f"Rank: `Error`\n"
            information += f"Level: `Error`\n"
            information += f"Karma: `{player['karma']}`\n"
            information += f"Experience: `{player['networkExp']:,}`\n"
            information += f"Votes: `{player['voting']['total']}`\n"
            if "achievements" in player:
                information += f"Achievements Completed: `{len(player['achievements'])}`\n"
            else:
                information += f"Achievement Points: `0`"
            information += f"Completed Parkour: `{len(player['parkourCompletions'])}`\n"
            information += f"Pending Friends: `{len(player['friendRequestsUuid'])}`\n"
            information += f"Version: `{player['mcVersionRp']}`\n"
            #information += f"Last Game: `{player['mostRecentGameType']}`\n"

            dates = ""
            dates += f"First Logon: `{datetime.datetime.fromtimestamp(player['firstLogin'] / 1e3).strftime('%b %d, %Y')}`\n"
            dates += f"Last Login: `{datetime.datetime.fromtimestamp(player['lastLogin'] / 1e3).strftime('%b %d, %Y')}`\n"
            dates += f"Last Logout: `{datetime.datetime.fromtimestamp(player['lastLogout'] / 1e3).strftime('%b %d, %Y')}`\n"

            embed.add_field(name=":newspaper:  INFORMATION", value=information)
            embed.add_field(name=":calendar:  DATES", value=dates, inline=False)
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/{uuid}")

            msg = await ctx.send(embed=embed)



            # might implement this some other day
            # I would like to say that I hate having emoji's in my code and don't understand why i can't use something like :newspaper: which works for everything else
            #await msg.add_reaction("📰")
            #await msg.add_reaction("💾")
            #await msg.add_reaction("🚩")


            #def check(reaction, user):
            #    return str(reaction.emoji) in ["📰", "💾", "🚩"] and user == ctx.message.author

            #try:
            #    while True:
            #        reaction, user = await self.bot.wait_for("reaction_add", timeout=10.0, check=check)
            #        if str(reaction.emoji) == "💾":
            #            guild()
            #        elif str(reaction.emoji) == "📰":
            #            profile()
            #        else:
            #            parkour()
            #except asyncio.TimeoutError:
            #    print("timeout")
            #except:
            #    print("error")
            

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
'''