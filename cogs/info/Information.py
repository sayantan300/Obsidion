from discord.ext import commands
from random import choice
import requests
import discord

from cogs.info.library import *


class Information(commands.Cog, name="Information"):

    @commands.command(aliases=['nameHistory', 'namehistory'])
    async def profile(self, ctx, username):
        """View a players Minecraft UUID, Username history and skin."""

        uuid = get_uuid(username)
        if uuid:
            long_uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16-20]}-{uuid[20:]}"

            usernames = names(uuid)[0:]

            embed = discord.Embed(title=f"Minecraft profile for {username}", color=0x00ff00)

            embed.add_field(name="Short UUID:", value=uuid)
            embed.add_field(name="Long UUID:", value=long_uuid)
            embed.add_field(name="Information", value=f"Username Changes:{len(names)}")
            embed.add_field(name="Name History", value="IN PROGRESS")
            embed.set_thumbnail(url=(f"https://visage.surgeplay.com/bust/{uuid}"))

            await ctx.send(embed=embed)
        else:
            await ctx.send("That username is not been used.")

    @commands.command()
    async def checkName(self, ctx, username):
        """Check weather a username is currently in use."""

        if get_uuid(username):
            # Need to add option to view profile with reaction
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name="Name Checker", value=f"The username: `{username}` is currently unavailable.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name="Name Checker", value=f"The username: `{username}` is available! \n Claim the username here: https://account.mojang.com/me")
            await ctx.send(embed=embed)

    @commands.command()
    async def uuid(self, ctx, username):
        """Get a players UUID."""

        uuid = get_uuid(username)
        if uuid:
            long_uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16-20]}-{uuid[20:]}"
            embed = discord.Embed(title=f"Showing {username}'s Minecraft UUID")
            embed.add_field(name=f"{username}'s UUID", value=f"Short UUID: `{uuid}` \n Long UUID:`{long_uuid}`")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: the user: `{username}` does not exist!")

    @commands.command()
    async def server(self, ctx, server):
        """Request a JAVA Minecraft server for information such as online player count, MOTD and more."""

        resposne = requests.get(f"https://mcapi.us/server/status?ip={server}")
        data = resposne.json()

        if data["online"] == "true":
            await ctx.send("Still in progress")
        else:
            await ctx.send(f"The server {server} is currently offline")

    @commands.command()
    async def serverPE(self, ctx, server):
        """equest a BEDROCK Minecraft server for information such as online player count, MOTD and more."""

        await ctx.send("Still in progress")

    @commands.command()
    async def status(self, ctx):
        """Check the status of all the Mojang services"""

        response = requests.get(url="https://status.mojang.com/check")
        data = response.json()

        embed = discord.Embed(title=f"Minecraft Service Status", color=0x00ff00)

        for state in data:
            embed.add_field(name=state[0], value=state[1])

        await ctx.send(embed=embed)

    @commands.command()
    async def version(self, ctx, username):
        """View all of Minecraft Java edition versions or a specific version."""
        
        await ctx.send("Still in progress")

    @commands.command()
    async def latestVersion(self, ctx, username):
        """View the latest version or snapshot within the Minecraft Java launcher."""

        await ctx.send("Still in progress")

    @commands.command()
    async def colors(self, ctx, username):
        """View all the text colors in Minecraft."""

        colors_list = {
            "Red":        {"id": 14, "hex": "#b02e26"},
            "Orange":     {"id": 1,  "hex": "#f9801d"},
            "Yellow":     {"id": 4,  "hex": "#fed83d"},
            "Lime":       {"id": 5,  "hex": "#80c71f"},
            "Green":      {"id": 13, "hex": "#5e7c16"},
            "Light Blue": {"id": 3,  "hex": "#3ab3da"},
            "Cyan":       {"id": 9,  "hex": "#169c9c"},
            "Blue":       {"id": 11, "hex": "#3c44aa"},
            "Purple":     {"id": 10, "hex": ""},
            "Magenta":    {"id": 2,  "hex": ""},
            "Pink":       {"id": 6,  "hex": ""},
            "White":      {"id": 0,  "hex": ""},
            "Light_Gray": {"id": 8,  "hex": ""},
            "Gray":       {"id": 7,  "hex": ""},
            "Black":      {"id": 15, "hex": ""},
            "Brown":      {"id": 12, "hex": ""}
        }

        await ctx.send("Still in progress")

    @commands.command()
    async def news(self, ctx, username):
        """See the latest post on Minecraft.net."""

        await ctx.send("Still in progress")

    @commands.command()
    async def sales(self, ctx):
        """View the amount of copies of Minecraft that have been sold"""

        payload = {
            'metricKeys': ["item_sold_minecraft"]
        }
        response = requests.get("https://api.mojang.com/orders/statistics", json=payload)

        await ctx.send("Still in progress")
