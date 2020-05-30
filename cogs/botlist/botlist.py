# Handles automatic posting
import dbl
import aiohttp
import config
import discord
from discord.ext import commands, tasks


async def post_stats(session, url, headers, json):
    async with session(headers=headers) as session:
        await session.post(url, json=json)


class bot_advertise(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session
        self.vote_channel = config.upvote_channel
        if config.bots4discordToken:
            self.bfdtoken = config.bots4discordToken
            self.bots4discordcount.start()
        if config.bots4discordToken:
            self.bfdtoken = config.bots4discordToken
            self.bots4discordcount.start()
        if config.dblToken:
            self.dbltoken = config.dblToken
            self.dblpy = dbl.DBLClient(self.bot, self.dbltoken, autopost=True)
        if config.boatstoken:
            self.boatstoken = config.boatstoken
            self.boats_server_count.start()

    # bots4discord
    @tasks.loop(seconds=60)
    async def bots4discordcount(self):
        await self.bot.wait_until_ready()
        url = f"https://botsfordiscord.com/api/bot/{self.bot.user.id}"
        headers = {"Authorization": self.bfdtoken}
        json = {"server_count": len(self.bot.guilds)}
        await post_stats(self.session, url, headers, json)

    # discord boats
    @tasks.loop(seconds=60)
    async def boats_server_count(self):
        await self.bot.wait_until_ready()
        url = f"https://discord.boats/api/bot/{self.bot.user.id}"
        headers = {"Authorization": self.boatstoken}
        json = {"server_count": len(self.bot.guilds)}
        await post_stats(self.session, url, headers, json)

    # discordbotlist
    @tasks.loop(seconds=60)
    async def boats_server_count(self):
        await self.bot.wait_until_ready()
        url = f"https://discordbotlist.com/api/v1/bots/{self.bot.user.id}/stats"
        headers = {"Authorization": self.discordbotlisttoken}
        json = {"guilds": len(self.bot.guilds)}
        await post_stats(self.session, url, headers, json)

    # discordlabs
    @tasks.loop(seconds=60)
    async def boats_server_count(self):
        await self.bot.wait_until_ready()
        url = f"https://bots.discordlabs.org/v2/bot/{self.bot.user.id}/stats"
        json = {"server_count": len(self.bot.guilds), "token": self.discordlabstoken}
        await post_stats(self.session, url, None, json)

    # botsondiscord
    @tasks.loop(seconds=60)
    async def boats_server_count(self):
        await self.bot.wait_until_ready()
        url = f"https://bots.ondiscord.xyz/bot-api/bots/{self.bot.user.id}/guilds"
        headers = {"Authorization": self.boatstoken}
        json = {"guildCount": len(self.bot.guilds)}
        await post_stats(self.session, url, headers, json)

    # # top.gg
    # @commands.Cog.listener()
    # async def on_dbl_vote(self, data):
    #     embed = discord.Embed(
    #         title=f"New upvote for {self.bot.user.name} on top.gg",
    #         description=f"<@{data['user']}> Has just upvoted {self.bot.user.name}!",
    #     )
    #     channel = self.bot.get_channel(self.vote_channel)
    #     await channel.send(embed=embed)
