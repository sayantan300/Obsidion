import logging
from datetime import datetime
import discord
from time import mktime

import feedparser
from discord.ext import commands, tasks

from obsidion.bot import Obsidion

categories = ("Deep Dives", "News", "Minecraft Builds", "Dungeons")

Minecraft_News_RSS = "https://www.minecraft.net/en-us/feeds/community-content/rss"

log = logging.getLogger(__name__)


class MinecraftNews(commands.Cog):
    """Post minecraft news"""

    def __init__(self, bot: Obsidion):
        self.bot = bot
        self.get_media.start()

    @tasks.loop(minutes=10)
    async def get_media(self) -> None:
        async with self.bot.http_session.get(Minecraft_News_RSS) as resp:
            text = await resp.text()
        data = feedparser.parse(text)
        latest_post = data["entries"][0]
        description = f"Summary: {latest_post['summary']}"
        embed = discord.Embed(
            title=latest_post["title_detail"]["value"],
            description=description,
            colour=0x00FF00,
            url=latest_post["id"],
        )
        embed.set_image(url=f"https://minecraft.net{latest_post['imageurl']}")
        embed.add_field(name="Category", value=latest_post["primarytag"])
        embed.set_footer(text="Article Published")
        embed.set_author(
            name="New Article on Minecraft.net",
            url=f"https://minecraft.net{latest_post['imageurl']}",
            icon_url="https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/img/menu/menu-buy--reversed.gif",
        )
        dt = datetime.fromtimestamp(mktime(latest_post["published_parsed"]))

        embed.timestamp = dt

        channel = self.bot.get_channel(725790318938685520)
        await channel.send(embed=embed)

    def cog_unload(self) -> None:
        """Stop news posting tasks on cog unload."""
        self.get_media.cancel()


def setup(bot: Obsidion) -> None:
    """Add `News` cog."""
    bot.add_cog(MinecraftNews(bot))
