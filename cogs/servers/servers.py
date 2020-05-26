from discord.ext import commands
import logging

log = logging.getLogger(__name__)


class servers(commands.Cog, name="Servers"):
    def __init__(self, bot):
        self.session = bot.session
        self.bot = bot

    # @commands.command()
    # async def blocksmcself(self, ctx, username):
    #    uuid = get_uuid(self.session, username)
    #    pass

    # @commands.command()
    # async def funcraft(self, ctx, username):


#    uuid = get_uuid(self.session, username)
#    pass

# @commands.command()
# async def hivemc(self, ctx, username):
#    pass

# @commands.command()
# async def hypixel(self, ctx, username):
#    """Get information about a Hypixel user"""
#    uuid = get_uuid(self.session, username)
#    pass

# @commands.command()
# async def manacube(self, ctx, username):
#    uuid = get_uuid(self.session, username)
#    pass

# @commands.command()
# async def minesage(self, ctx, username):
#    pass

# @commands.command()
# async def universocraft(self, ctx, username):
#    pass
# @commands.command()
# async def veltpvp(self, ctx, username):
#    pass

# @commands.command()
# async def wynncraft(self, ctx, username):
#    uuid = get_uuid(self.session, username)
#    pass

