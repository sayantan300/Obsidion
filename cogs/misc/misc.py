from discord.ext import commands
from random import choice
import discord
import resource
import json

class Miscellaneous(commands.Cog, name="Miscellaneous"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def invite(self, ctx):
        """Provied the link to invite the bot to your server"""
        embed = discord.Embed(description="**[Add the bot To Your Discord Server](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot)**", color=0x00ff00)
        await ctx.send(embed=embed)
        pass

    @commands.command()
    async def ping(self, ctx):
        """Check ping of client, message and api"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="Bot's Ping", color=0x00ff00)
        embed.add_field(name="API Ping", value=f"`{latency}ms`")

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        """View statistics about the bot"""
        total_users = 0
        channels = 0
        for guild in self.bot.guilds:
            total_users += len(guild.members)
            channels += len(guild.text_channels)
            channels += len(guild.voice_channels)

        ram = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (2**20), 2)

        statics = ""
        statics += f"Guilds: `{len(self.bot.guilds):,}`\n"
        statics += f"Users: `{total_users:,}`\n"
        statics += f"Channels: `{channels:,}`\n"
        statics += f"Memory Usage: `{ram:,}MB`\n"
        statics += f"Discord.py: `v{discord.__version__}`"

        links = ""
        links += "[INVITE BOT](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot)\n"
        links += "[GITHUB](https://github.com/Darkflame72/Minecraft-Discord)"

        embed = discord.Embed(title="Stats", color=0x00ff00)
        embed.add_field(name=":newspaper: STATS", value=statics, inline=True)
        embed.add_field(name=":link: LINKS", value=links, inline=True)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *cog_name):
        """Gets all cogs and commands of mine."""
        if cog_name:
            if len(cog_name) > 1:
                await ctx.send(f"{ctx.message.author.mention}, :x: Please enter only one command for help")
            else:
                # get information on 1 cog
                cog_name = cog_name[0]
                found=False
                for x in self.bot.cogs:
                    for y in self.bot.get_cog(x).get_commands():
                        if y.name == cog_name:
                            embed = discord.Embed(title=cog_name, description=y.help, color=0x00ff00)
                            await ctx.author.send(embed=embed)
                            found=True
                            break
                if not found:
                    await ctx.send(f"{ctx.message.author.mention}, :x: That command is not found please try again")
        else:
            with open("data.json", "r+") as f:
                json_data = json.load(f)
            prefix = json_data["server"][str(ctx.guild.id)]
            embed = discord.Embed(description=f"Below is a list of commands you can use\n To get more information about a command type: `{prefix}help command`", color=0x00ff00)
            embed.set_author(name="Bot's Commands")
            # General help command
            for cog in self.bot.cogs:
                cogs=[]
                cog_commands = self.bot.get_cog(cog).get_commands()
                for c in cog_commands:
                    cogs.append(c.name)
                embed.add_field(name=cog, value=f"`{'`, `'.join(cogs)}`", inline=False)
            embed.set_footer(text="Version: 0.1 | Authors: Darkflame72#1150")
            await ctx.send(embed=embed)