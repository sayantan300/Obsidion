from cogs.config.Config import Configurable


def setup(bot):
    bot.add_cog(Configurable(bot))
