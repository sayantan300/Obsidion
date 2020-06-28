from discord.ext import commands
from asyncrcon import AsyncRCON, AuthenticationException


class rcon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rsend(self, ctx: commands.Context, addr: str, pw: str, message: str):
        """Send an rcon message to a minecraft server."""
        await ctx.trigger_typing()

        rcon = AsyncRCON(addr, pw)
        try:
            await rcon.open_connection()
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await rcon.command(message)
        await ctx.send(res)

        rcon.close()
