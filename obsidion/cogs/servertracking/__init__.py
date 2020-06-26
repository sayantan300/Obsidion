from .servertracking import servertracking


def setup(bot):
    bot.add_cog(servertracking(bot))
