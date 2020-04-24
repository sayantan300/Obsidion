from cogs.botlist.botlist import bot_advertise


def setup(bot):
    bot.add_cog(bot_advertise(bot))
