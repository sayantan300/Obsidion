from discord.ext import commands
from random import choice
import discord
import aiohttp
from datetime import datetime


async def get(session, url):
    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data
        else:
            return False


async def get_uuid(session, username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.json()
            uuid = data["id"]
            return uuid
        else:
            return False


class Information(commands.Cog, name="Information"):

    def __init__(self, bot):
        self.session = bot.session

    @commands.command(aliases=['whois', 'p', "names", "namehistory", "pastnames", "namehis"])
    async def profile(self, ctx, username):
        """View a players Minecraft UUID, Username history and skin."""

        uuid = await get_uuid(self.session, username)

        if uuid:
            long_uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

            url = f"https://api.mojang.com/user/profiles/{uuid}/names"
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    names = await resp.json()

            name_list = ""
            for name in names[::-1][:-1]:
                name1 = name["name"]
                # Prettify and give actual month and time passed @Cubic_dd#9976
                date = datetime.utcfromtimestamp(
                    int(str(name["changedToAt"])[:-3])).strftime('%b %d, %Y')
                name_list += f"**{names.index(name)+1}.** `{name1}` - {date} " + "\n"
            original = names[0]["name"]
            name_list += f"**1.** `{original}` - First Username"

            uuids = "Short UUID: `" + uuid + "\n" + "`Long UUID: `" + long_uuid + "`"

            embed = discord.Embed(
                title=f"Minecraft profile for {username}", color=0x00ff00)

            embed.add_field(name="UUID's", inline=False, value=uuids)
            embed.add_field(name="Textures", inline=True,
                            value=f"Skin: [Open Skin](https://visage.surgeplay.com/bust/{uuid})")
            embed.add_field(name="Information", inline=True,
                            value=f"Username Changes: {len(names)-1}")
            embed.add_field(name="Name History", inline=False, value=name_list)
            embed.set_thumbnail(
                url=(f"https://visage.surgeplay.com/bust/{uuid}"))

            await ctx.send(embed=embed)
        else:
            await ctx.send("That username is not been used.")

    @commands.command(aliases=["available", "availability", "namecheck"])
    async def checkname(self, ctx, username):
        """Check weather a username is currently in use."""

        if await get_uuid(self.session, username):
            # Need to add option to view profile with reaction
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(
                name="Name Checker", value=f"The username: `{username}` is currently unavailable.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(
                name="Name Checker", value=f"The username: `{username}` is available! \n Claim the username here: https://account.mojang.com/me")
            await ctx.send(embed=embed)

    @commands.command()
    async def uuid(self, ctx, username):
        """Get a players UUID."""

        uuid = await get_uuid(self.session, username)
        if uuid:
            long_uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16-20]}-{uuid[20:]}"
            embed = discord.Embed(
                title=f"Showing {username}'s Minecraft UUID", color=0x00ff00)
            embed.add_field(
                name=f"{username}'s UUID", value=f"Short UUID: `{uuid}` \n Long UUID:  `{long_uuid}`")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: the user: `{username}` does not exist!")

    @commands.command()
    async def server(self, ctx, server):
        """Request a JAVA Minecraft server for information such as online player count, MOTD and more."""

        data = await get(self.session, f"https://api.mcsrvstat.us/2/{server}")
        if data["online"] == True:
            embed = discord.Embed(
                title=f"Java Server: {server}", color=0x00ff00)
            # need to fix encoding issues
            embed.add_field(name="Description", value=data["motd"]["raw"][0])
            now = data["players"]["online"]
            max = data["players"]["max"]
            embed.add_field(
                name="Players", value=f"Online: `{now:,}` \n Maximum: `{max:,}`")
            if now > 10 or now == 0:
                pass
            else:
                names = "\n".join(data["players"]["list"])
                embed.add_field(name="Player names", value=names)

            if 'software' in data:
                version = f"{data['software']} {data['version']}"
            else:
                version = data['version']

            embed.add_field(
                name="Version", value=f"Java Edition \n Running: `{version}` \n Protocol: `{data['protocol']}`", inline=False)

            embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{server}")

            await ctx.send(embed=embed)
        else:
            print(data["online"])
            await ctx.send(f"{ctx.author}, :x: The Jave edition Minecraft server `{server}` is currently not online or cannot be requested")

    @commands.command()
    async def status(self, ctx):
        """Check the status of all the Mojang services"""

        data = await get(self.session, "https://status.mojang.com/check")

        sales_mapping = {
            'item_sold_minecraft': True,
            'prepaid_card_redeemed_minecraft': True,
            'item_sold_cobalt': False,
            'item_sold_scrolls': False
        }
        payload = {
            'metricKeys': [k for (k, v) in sales_mapping.items() if v]
        }

        url = "https://api.mojang.com/orders/statistics"
        async with self.session.post(url, json=payload) as resp:
            if resp.status == 200:
                sales_data = await resp.json()

        embed = discord.Embed(
            title=f"Minecraft Service Status", color=0x00ff00)
        embed.add_field(name="Minecraft Game Sales",
                        value=f"Total Sales: **{sales_data['total']:,}** Last 24 Hours: **{sales_data['last24h']:,}**")

        services = ""
        for service in data:
            if service[next(iter(service))] == "green":
                services += f":green_heart: - {next(iter(service)).title()}: **This service is healthy.** \n"
            elif service[next(iter(service))] == "yellow":
                services += f":yellow_heart: - {next(iter(service)).title()}: **This service has some issues.** \n"
            else:
                services += f":heart: - {next(iter(service)).title()}: **This service is offline.** \n"
        embed.add_field(name="Minecraft Services:",
                        value=services, inline=False)

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

        url = f"https://api.mojang.com/orders/statistics"
        async with self.session.post(url, json=payload) as resp:
            if resp.status == 200:
                sales_data = await resp.json()

        embed = discord.Embed(color=0x00ff00)

        sale = f"Total Sales: `{sales_data['total']:,}`\n"
        sale += f"Sales in the last 24 hours: `{sales_data['last24h']:,}`\n"
        sale += f"Sales per second: `{sales_data['saleVelocityPerSeconds']}`\n"
        sale += "[BUY MINECRAFT](https://my.minecraft.net/en-us/store/minecraft/)"

        embed.add_field(name="Minecraft Sales", value=sale)

        await ctx.send(embed=embed)

    @commands.command(aliases=["uhcgg", "uhc.gg"])
    async def uhc(self, ctx, command, info=None):
        """View info about uhc matches"""
        if command == "upcoming":
            data = await get(self.session, "https://hosts.uhc.gg/api/matches/upcoming")

            embed = discord.Embed(title="UHC.gg upcoming UHC games", description="Displayed the top 6 upcoming UHC games on [hosts.uhc.gg](https://hosts.uhc.gg)\n", color=0x00ff00)

            for match in data[:6]:
                address = match['address']
                opens = match['opens']
                author = match['author']
                region = match['region']
                version = match['version']
                slots = match['slots']
                length = match['length']
                tournament = match['tournament']
                id = match['id']

                info = ""
                info += f"Opens: {opens}\n"
                info += f"Author: {author}\n"
                info += f"Region: {region}\n"
                info += f"Version: {version}\n"
                info += f"Slots: {slots}\n"
                info += f"Length: {length} minutes\n"
                info += f"Tournament: {tournament}\n"
                info += f"id: {id}"

                embed.add_field(name=address, value=info)

            await ctx.send(embed=embed)


    # @commands.command()
    # async def version(self, ctx, version):
        #"""View all of Minecraft Java edition versions or a specific version."""

        # await ctx.send("Still in progress")

    # @commands.command(aliases=["latestver", "latestversion"])
    # async def latest(self, ctx, snapshot):
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

    # @commands.command(aliases=["latestarticle", "minecraftnews", "latestnews"])
    # async def news(self, ctx):
    #    """See the latest post on Minecraft.net."""
    #
    #    await ctx.send("Still in progress")
