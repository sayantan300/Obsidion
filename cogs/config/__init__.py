from cogs.config.config import Configurable


def setup(bot):
    bot.add_cog(Configurable(bot))
