# Handles automatic posting
import dbl
import aiohttp
import config
import asyncio
import discord
from discord.ext import commands


class bot_advertise(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vote_channel = config.upvote_channel
        if config.bots4discordToken:
            self.bfdtoken = config.bots4discordToken
            self.bg_task = bot.loop.create_task(self.loop_server_count())
        if config.dblToken:
            self.dbltoken = config.dblToken
            self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    async def loop_server_count(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            url = f"https://botsfordiscord.com/api/bot/{self.bot.user.id}"
            headers = {"Authorization": self.bfdtoken}
            json = {"server_count": len(self.bot.guilds)}
            async with aiohttp.ClientSession(headers=headers) as session:
                await session.post(url, json=json)
            await asyncio.sleep(600)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        embed = discord.Embed(
            title=f"New upvote for {self.bot.user.name} on top.gg",
            description=f"<@{data['user']}> Has just upvoted {self.bot.user.name}!",
        )
        channel = self.bot.get_channel(self.vote_channel)
        await channel.send(embed=embed)
