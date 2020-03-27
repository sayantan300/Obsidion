from discord.ext import commands
from random import choice
import discord
import aiohttp
import requests
from datetime import datetime
import base64

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

    @commands.command(aliases=['whois', 'p', "names", "namehistory", "pastnames", "namehis"])
    async def profile(self, ctx, username):
        """View a players Minecraft UUID, Username history and skin."""

        uuid = get_uuid(username)
        if uuid:
            long_uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

            names = get(f"https://api.mojang.com/user/profiles/{uuid}/names")

            name_list=""
            for name in names[::-1][:-1]:
                name1 = name["name"]
                date = datetime.utcfromtimestamp(int(str(name["changedToAt"])[:-3])).strftime("%Y-%m-%d %H:%M:%S (UTC)") # Prettify and give actual month and time passed @Cubic_dd#9976
                name_list += f"**{names.index(name)+1}.** `{name1}` - {date} "+ "\n"
            original = names[0]["name"]
            name_list+=f"**1.** `{original}` - First Username"

            uuids = "Short UUID: `" + uuid + "\n" + "`Long UUID: `" + long_uuid + "`"

            embed = discord.Embed(title=f"Minecraft profile for {username}", color=0x00ff00)

            embed.add_field(name="UUID's", inline=False, value=uuids)
            embed.add_field(name="Textures", inline=True, value=f"Skin: [Open Skin](https://visage.surgeplay.com/bust/{uuid})")
            embed.add_field(name="Information", inline=True, value=f"Username Changes: {len(names)-1}")
            embed.add_field(name="Name History", inline=False, value=name_list)
            embed.set_thumbnail(url=(f"https://visage.surgeplay.com/bust/{uuid}"))

            await ctx.send(embed=embed)
        else:
            await ctx.send("That username is not been used.")

    @commands.command(aliases=["available", "availability", "namecheck"])
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
            embed.add_field(name=f"{username}'s UUID", value=f"Short UUID: `{uuid}` \n Long UUID:  `{long_uuid}`")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: the user: `{username}` does not exist!")

    
    @commands.command()
    async def server(self, ctx, server):
        """Request a JAVA Minecraft server for information such as online player count, MOTD and more."""

        data = get(f"https://api.mcsrvstat.us/2/{server}")
        if data["online"] == True:
            embed = discord.Embed(title=f"Java Server: {server}", color=0x00ff00)
            embed.add_field(name="Description", value=data["motd"]["raw"][0]) # need to fix encoding issues
            now = data["players"]["online"]
            max = data["players"]["max"]
            embed.add_field(name="Players", value=f"Online: `{now:,}` \n Maximum: `{max:,}`")
            if now > 10 or now == 0:
                pass
            else:
                names = "\n".join(data["players"]["list"])
                embed.add_field(name="Player names", value=names)
            #imagedata = base64.b64decode(data["favicon"][22:])
            #filename = 'favicon.png'  # I assume you have a way of picking unique filenames
            #with open(filename, 'wb') as f:
            #    f.write(imagedata)
            #embed.set_thumbnail(url=("attachment://favicon.png"))
            embed.add_field(name="Version", value=data['version'])

            await ctx.send(embed=embed)
        else:
            print(data["online"])
            await ctx.send(f"{ctx.author}, :x: The Jave edition Minecraft server `{server}` is currently not online or cannot be requested")

    @commands.command()
    async def status(self, ctx):
        """Check the status of all the Mojang services"""

        data = get("https://status.mojang.com/check")

        sales_mapping = {
        'item_sold_minecraft': True,
        'prepaid_card_redeemed_minecraft': True,
        'item_sold_cobalt': False,
        'item_sold_scrolls': False
        }
        payload = {
            'metricKeys': [k for (k, v) in sales_mapping.items() if v]
        }

        sales_data = requests.post("https://api.mojang.com/orders/statistics", json=payload).json()


        embed = discord.Embed(title=f"Minecraft Service Status", color=0x00ff00)
        embed.add_field(name="Minecraft Game Sales", value=f"Total Sales: **{sales_data['total']:,}** Last 24 Hours: **{sales_data['last24h']:,}**")


        services = ""
        for service in data:
            if service[next(iter(service))] == "green":
                services += f":green_heart: - {next(iter(service)).title()}: **This service is healthy.** \n"
            elif service[next(iter(service))] == "yellow":
                services += f":yellow_heart: - {next(iter(service)).title()}: **This service has some issues.** \n"
            else:
                services +=f":heart: - {next(iter(service)).title()}: **This service is offline.** \n"
        embed.add_field(name="Minecraft Services:", value=services, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def sales(self, ctx):
        """See the total sales of Minecraft"""
        sales_mapping = {
            'item_sold_minecraft': True,
            'prepaid_card_redeemed_minecraft': True,
            'item_sold_cobalt': False,
            'item_sold_scrolls': False
        }
        payload = {
            'metricKeys': [k for (k, v) in sales_mapping.items() if v]
        }

        sales_data = requests.post("https://api.mojang.com/orders/statistics", json=payload).json()

        embed = discord.Embed(color=0x00ff00)

        sale = f"Total Sales: `{sales_data['total']:,}`\n"
        sale += f"Sales in the last 24 hours: `{sales_data['last24h']:,}`\n"
        sale += f"Sales per second: `{sales_data['saleVelocityPerSeconds']}`\n"
        sale += "[BUY MINECRAFT](https://my.minecraft.net/en-us/store/minecraft/)"

        embed.add_field(name="Minecraft Sales", value=sale)

        await ctx.send(embed=embed)



    #@commands.command()
    #async def version(self, ctx, version):
        #"""View all of Minecraft Java edition versions or a specific version."""

        #await ctx.send("Still in progress")

    #@commands.command(aliases=["latestver", "latestversion"])
    #async def latest(self, ctx, snapshot):
    #    """View the latest version or snapshot within the Minecraft Java launcher."""

    #    embed = discord.Embed(title="Latest JAVA release", color=0x00ff00)

    #    current = ""
    #    current += f"Version: `{}`\n"
    #    current += f"Latest Snapshot: `{}`"
    #    embed.add_field(name="Current Release", value="")

    #    latest = 0
    #    latest += f"{}\n"
    #    latest += f"Time Published: `{}`\n"
    #    latest += f"Type: `{}`\n"
    #    latest += f"URL: [{} | snapshot]({})"

    #    embed.add_field(name="Latest Version", value=latest)
        
    #    await ctx.send(embed=embed)

    #@commands.command(aliases=["latestarticle", "minecraftnews", "latestnews"])
    #async def news(self, ctx):
    #    """See the latest post on Minecraft.net."""
    #
    #    await ctx.send("Still in progress")