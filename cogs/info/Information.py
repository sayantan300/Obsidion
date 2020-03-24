from discord.ext import commands
from random import choice
import discord
import aiohttp
import requests

def get(url):
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return False

def get_uuid(username):
    r = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

    if r.status_code == 200:
        data = r.json()
        uuid = data["id"]
        return uuid
    else:
        return False


class Information(commands.Cog, name="Information"):

    @commands.command(aliases=['nameHistory', 'namehistory'])
    async def profile(self, ctx, username):
        """View a players Minecraft UUID, Username history and skin."""

        uuid = get_uuid(username)
        if uuid:
            long_uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16-20]}-{uuid[20:]}"

            names = get(f"https://api.mojang.com/user/profiles/{uuid}/names")

            name_list=""
            for name in names[::-1][:-1]:
                name1 = name["name"]
                date = name["changedToAt"]
                name_list = f"**{names.index(name)+1}.** `{name1}` - {date} "+ "\n" + name_list
            original = names[0]["name"]
            name_list=f"**1.** `{original}` - First Username" + "\n" + name_list

            uuids = "Short UUID: `" + uuid + "\n" + "`Long UUID: `" + long_uuid + "`"

            embed = discord.Embed(title=f"Minecraft profile for {username}", color=0x00ff00)

            embed.add_field(name="UUID's", inline=False, value=uuids)
            embed.add_field(name="Textures", inline=True, value=f"Skin: https://visage.surgeplay.com/bust/{uuid}" )
            embed.add_field(name="Information", inline=True, value=f"Username Changes: {len(names)}")
            embed.add_field(name="Name History", inline=False, value=name_list)
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
            embed = discord.Embed(title=f"Showing {username}'s Minecraft UUID", color=0x00ff00)
            embed.add_field(name=f"{username}'s UUID", value=f"Short UUID: `{uuid}` \n Long UUID:`{long_uuid}`")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: the user: `{username}` does not exist!")

    @commands.command()
    async def server(self, ctx, server):
        """Request a JAVA Minecraft server for information such as online player count, MOTD and more."""

        data = get(f"https://mcapi.us/server/status?ip={server}")

        if data["online"] == "True":
            await ctx.send("Still in progress")
        else:
            await ctx.send(f"The server {server} is currently offline")

    @commands.command()
    async def serverPE(self, ctx, server):
        """request a BEDROCK Minecraft server for information such as online player count, MOTD and more."""

        await ctx.send("Still in progress")

    @commands.command()
    async def status(self, ctx):
        """Check the status of all the Mojang services"""

        data = get("https://status.mojang.com/check")


        embed = discord.Embed(title=f"Minecraft Service Status", color=0x00ff00)

        for state in data:
            if state[state.keys()[0]] == "red":
                embed.add_field(name=state[0], value=state[1])

        #embed.add_field(name=state[0], value=state[1])
        #embed.add_field(name=state[0], value=state[1])
        #embed.add_field(name=state[0], value=state[1])
        #embed.add_field(name=state[0], value=state[1])
        #embed.add_field(name=state[0], value=state[1])
        #embed.add_field(name=state[0], value=state[1])
        #embed.add_field(name=state[0], value=state[1])
        #embed.add_field(name=state[0], value=state[1])

        #for state in data:
            #embed.add_field(name=state[0], value=state[1])

        await ctx.send("Still in progress")

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
    async def mcseen(self, ctx, username):
        """last seen"""

        await ctx.send("Still in progress")