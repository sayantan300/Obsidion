from cogs.admin.admin import admin, bot_advertise

def setup(bot):
    bot.add_cog(admin(bot))
    bot.add_cog(bot_advertise(bot))


#from cogs.admin.admin import TopGG

#def setup(bot):
#    bot.add_cog(TopGG(bot))

