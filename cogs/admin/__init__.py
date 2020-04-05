from cogs.admin.admin import admin, bots4discord

def setup(bot):
    bot.add_cog(admin(bot))
    bot.add_cog(bots4discord(bot))


#from cogs.admin.admin import TopGG

#def setup(bot):
#    bot.add_cog(TopGG(bot))

