from discord.ext import commands
from random import choice
import discord

class Miscellaneous(commands.Cog, name="Miscellaneous"):

    @commands.command()
    async def invite(self, ctx):
        """Provied the link to invite the bot to your server"""
        embed = discord.Embed(description="**[Add the bot To Your Discord Server](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot)**", color=0x00ff00)
        await ctx.send(embed=embed)
        pass

    @commands.command()
    async def ping(self, ctx):
        """Check ping of client, message and api"""
        embed = discord.Embed(title="Bot's Ping", color=0x00ff00)
        embed.add_field(name="Client Ping", value=self.latency())
        #embed.add_field(name="Message Ping")
        #embed.add_field(name="API Ping")

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        """View statistics about the bot"""
        embed = discord.Embed(title="Stats", color=0x00ff00)

        #embed.add_field(name="Guilds", value=f"`{len(list(ctx.guilds))}`")
        #embed.add_field(name="Users", value=f"`{}`")
        #embed.add_field(name="Channels")
        embed.add_field(name="Discord.py", value=f"`{discord.__version__}`")
        
        await ctx.send(embed=embed)