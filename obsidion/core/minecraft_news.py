import logging
import typing as t
from discord.ext.commands import Cog
from obsidion.bot import Obsidion

Minecraft_News_RSS = "https://www.minecraft.net/en-us/feeds/community-content/rss"

log = logging.getLogger(__name__)


class MinecraftNews(Cog):
    """Post new PEPs and Python News to `#python-news`."""

    # TODO

    def cog_unload(self) -> None:
        """Stop news posting tasks on cog unload."""
        self.fetch_new_media.cancel()


def setup(bot: Obsidion) -> None:
    """Add `News` cog."""
    bot.add_cog(MinecraftNews(bot))
