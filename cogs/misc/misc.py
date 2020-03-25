from discord.ext import commands
from random import choice
import discord

class Miscellaneous(commands.Cog, name="Miscellaneous"):

    @commands.command()
    async def aliases(self, ctx):
        pass

    #@commands.command()
    #async def help(self, ctx):
    #    pass

    @commands.command()
    async def invite(self, ctx):
        """Provied the link to invite the bot to your server"""
        embed = discord.Embed( color=0x00ff00)
        embed.add_field(name="Invite link: ", value="[Invite Link](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot)")

        ctx.send(embed=embed)
        pass

    @commands.command()
    async def ping(self, ctx):
        """Check ping of client, message and api"""
        embed = discord.Embed(title="Bot's Ping", color=0x00ff00)
        embed.add_field(name="Client Ping" f"`bot.latency`")
        #embed.add_field(name="Message Ping")
        #embed.add_field(name="API Ping")

        ctx.send(embed=embed)
        pass

    @commands.command()
    async def stats(self, ctx):
        pass

    @commands.command()
    async def tutorial(self, ctx):
        pass