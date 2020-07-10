from .hivestats import hivestats


def setup(bot):
    bot.add_cog(hivestats(bot))
