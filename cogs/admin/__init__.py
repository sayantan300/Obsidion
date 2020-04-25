from cogs.admin.admin import admin


def setup(bot):
    bot.add_cog(admin(bot))
