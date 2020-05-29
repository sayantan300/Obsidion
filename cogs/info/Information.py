from discord.ext import commands
import discord
import datetime
from utils.utils import uuid_from_username, get
from uuid import UUID
import base64
import io
import re
import logging
import config
from utils.chat_formatting import *

log = logging.getLogger(__name__)

colours = {
    "black": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "dark_blue": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "dark_green": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "dark_green": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "dark_aqua": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "dark_red": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "dark_purple": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "gold": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "gray": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "dark_gray": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "blue": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "green": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "aqua": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "red": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "light_purple": {"code": "§0", "rgb": "000", "background-rgb": "",},
    "yellow": {"code": "§0", "rgb": "000", "background-rgb": ""},
    "white": {"code": "§0", "rgb": "000", "background-rgb": ""},
}


class Information(commands.Cog, name="Information"):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session
        self.api = config.api

    @commands.command(
        aliases=["whois", "p", "names", "namehistory", "pastnames", "namehis"]
    )
    async def profile(self, ctx, username=None):
        """View a players Minecraft UUID, Username history and skin."""
        await ctx.channel.trigger_typing()
        uuid, username = await uuid_from_username(username, self.session, self.bot, ctx)
        if uuid:
            data = await get(self.session, f"{self.api}/profile/{uuid}")
        else:
            data = False
        if uuid and data:
            long_uuid = (
                f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
            )

            names = data["names"]

            name_list = ""
            for name in names[::-1][:-1]:
                name1 = name["name"]
                date = datetime.datetime.utcfromtimestamp(
                    int(str(name["changedToAt"])[:-3])
                ).strftime("%b %d, %Y")
                name_list += f"**{names.index(name)+1}.** `{name1}` - {date} " + "\n"
            original = names[0]["name"]
            name_list += f"**1.** `{original}` - First Username"

            uuids = "Short UUID: `" + uuid + "\n" + "`Long UUID: `" + long_uuid + "`"
            information = ""
            information = (
                f"Username Changes: `{len(names)-1}`\n"
                f"Legacy: `{data['legacy']}`\n"
                f"Cached: `{datetime.datetime.utcfromtimestamp(float(data['cachetime'])):%H:%M:%S}`"
            )

            embed = discord.Embed(
                title=f"Minecraft profile for {username}", color=0x00FF00
            )

            embed.add_field(name="UUID's", inline=False, value=uuids)
            embed.add_field(
                name="Textures",
                inline=True,
                value=f"Skin: [Open Skin](https://visage.surgeplay.com/bust/{uuid})",
            )
            embed.add_field(name="Information", inline=True, value=information)
            embed.add_field(name="Name History", inline=False, value=name_list)
            embed.set_thumbnail(url=(f"https://visage.surgeplay.com/bust/{uuid}"))

            await ctx.send(embed=embed)
        else:
            await ctx.send("That username is not been used.")

    @commands.command(aliases=["serv"])
    async def server(self, ctx, server=None):
        """
        Request information about a Minecraft Java edition multiplayer server.
        """
        await ctx.channel.trigger_typing()
        if (
            server
            or ctx.guild
            and await self.bot.pool.fetchval(
                "SELECT server FROM guild WHERE id = $1", ctx.guild.id
            )
        ):
            server = (
                server
                if server
                else await self.bot.pool.fetchval(
                    "SELECT server FROM guild WHERE id = $1", ctx.guild.id
                )
            )
            url = f"{self.api}/server/java"
            if len(server.split(":")) == 2:
                payload = {
                    "server": server.split(":")[0],
                    "port": server.split(":")[1],
                }
            else:
                payload = {"server": server.split(":")[0]}
            async with self.session.get(url, params=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                else:
                    data = False
            if data:
                embed = discord.Embed(title=f"Java Server: {server}", color=0x00FF00)
                embed.add_field(name="Description", value=data["description"])

                embed.add_field(
                    name="Players",
                    value=f"Online: `{data['players']['online']:,}` \n Maximum: `{data['players']['max']:,}`",
                )
                if data["players"]["sample"]:
                    names = ""
                    for player in data["players"]["sample"]:
                        names += f"{player['name']}\n"
                    embed.add_field(name="Information", value=names, inline=False)
                embed.add_field(
                    name="Version",
                    value=f"Java Edition \n Running: `{data['version']['name']}` \n Protocol: `{data['version']['protocol']}`",
                    inline=False,
                )
                if data["favicon"]:
                    encoded = base64.decodebytes(data["favicon"][22:].encode("utf-8"))
                    image_bytesio = io.BytesIO(encoded)
                    favicon = discord.File(image_bytesio, "favicon.png")
                    embed.set_thumbnail(url="attachment://favicon.png")
                    await ctx.send(embed=embed, file=favicon)
                else:
                    await ctx.send(embed=embed)
            else:
                await ctx.send(
                    f"{ctx.author}, :x: The Jave edition Minecraft server `{server}` is currently not online or cannot be requested"
                )
        else:
            await ctx.send(f"{ctx.author}, :x: Please provide a server")

    @commands.command(aliases=["servpe"])
    async def serverpe(self, ctx, server=None):
        """Get information about a Bedrock Edition Server"""
        if server:
            host, port = server.split(":")
            print(self.api)
            url = f"{self.api}/server/bedrock"
            if len(server.split(":")) == 2:
                payload = {
                    "server": host,
                    "port": port,
                }
            else:
                payload = {"server": host}
            async with self.session.get(url, params=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()

            if data:
                embed = discord.Embed(title=f"Bedrock Server: {host}", color=0x00FF00)
                # cleanup motd very badly but it does it
                embed.add_field(name="Description", value=data["motd"], inline=False)
                embed.add_field(
                    name="Players",
                    value=f"Online: `{data['CurrentPlayers']}`\nMax: `{data['MaxPlayers']}`",
                )
                embed.add_field(
                    name="Version",
                    value=f"Bedrock Edition\nRunning: `{data['GameVersion']}`",
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    f"{ctx.author}, :x: The Bedrock edition Minecraft server `{server}` is currently not online or cannot be requested"
                )
        else:
            await ctx.send(f"{ctx.author}, :x: Please provide a server")

    @commands.command()
    async def status(self, ctx):
        """Check the status of all the Mojang services"""
        await ctx.channel.trigger_typing()
        data = await get(self.session, f"{config.api}/mojang/check")
        sales_mapping = {
            "item_sold_minecraft": True,
            "prepaid_card_redeemed_minecraft": True,
            "item_sold_cobalt": False,
            "item_sold_scrolls": False,
        }
        payload = {"metricKeys": [k for (k, v) in sales_mapping.items() if v]}

        url = "https://api.mojang.com/orders/statistics"
        async with self.session.post(url, json=payload) as resp:
            if resp.status == 200:
                sales_data = await resp.json()

        embed = discord.Embed(title="Minecraft Service Status", color=0x00FF00)
        embed.add_field(
            name="Minecraft Game Sales",
            value=f"Total Sales: **{sales_data['total']:,}** Last 24 Hours: **{sales_data['last24h']:,}**",
        )
        services = ""
        for service in data:
            if data[service] == "green":
                services += (
                    f":green_heart: - {service}: **This service is healthy.** \n"
                )
            else:
                services += f":heart: - {service}: **This service is offline.** \n"
        embed.add_field(name="Minecraft Services:", value=services, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def sales(self, ctx):
        """See the total sales of Minecraft"""
        await ctx.channel.trigger_typing()
        sales_mapping = {
            "item_sold_minecraft": True,
            "prepaid_card_redeemed_minecraft": True,
            "item_sold_cobalt": False,
            "item_sold_scrolls": False,
        }
        payload = {"metricKeys": [k for (k, v) in sales_mapping.items() if v]}

        url = "https://api.mojang.com/orders/statistics"
        async with self.session.post(url, json=payload) as resp:
            if resp.status == 200:
                sales_data = await resp.json()
            else:
                sales_data = False

        if sales_data:

            embed = discord.Embed(color=0x00FF00)

            sale = (
                f"Total Sales: `{sales_data['total']:,}`\n"
                f"Sales in the last 24 hours: `{sales_data['last24h']:,}`\n"
                f"Sales per second: `{sales_data['saleVelocityPerSeconds']}`\n"
                "[BUY MINECRAFT](https://my.minecraft.net/en-us/store/minecraft/)"
            )

            embed.add_field(name="Minecraft Sales", value=sale)

            await ctx.send(embed=embed)
        else:
            ctx.send(
                f"{ctx.author}, :x: the Mojang API is not currently available please try again soon"
            )

    @commands.group(aliases=["uhcgg", "uhc.gg"])
    async def uhc(self, ctx):
        """
        View info about uhc matches

        :param command: Chooses what request to make option are:`upcoming`
        """
        if ctx.invoked_subcommand is None:
            if ctx.guild is None:
                prefix = "/"
            else:
                prefix = ctx.prefix
            embed = discord.Embed(
                title="Command Usage",
                description=f"`{prefix}uhc upcoming` - Shows 6 upcoming matches.\n`{prefix}uhc banned <uuid | username>` - View the bans of a player.",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)

    @uhc.command(name="upcoming")
    async def uhc_upcoming(self, ctx):
        await ctx.channel.trigger_typing()
        data = await get(self.session, "https://hosts.uhc.gg/api/matches/upcoming")

        embed = discord.Embed(
            title="UHC.gg upcoming UHC games",
            description="Displayed the top 6 upcoming UHC games on [hosts.uhc.gg](https://hosts.uhc.gg)\n",
            color=0x00FF00,
        )

        for match in data[:6]:
            address = match["address"]
            opens = match["opens"]
            author = match["author"]
            region = match["region"]
            version = match["version"]
            slots = match["slots"]
            length = match["length"]
            tournament = match["tournament"]
            match_id = match["id"]

            info = (
                f"Opens: {opens}\n"
                f"Author: {author}\n"
                f"Region: {region}\n"
                f"Version: {version}\n"
                f"Slots: {slots}\n"
                f"Length: {length} minutes\n"
                f"Tournament: {tournament}\n"
                f"id: {match_id}"
            )

            embed.add_field(name=address, value=info)

        await ctx.send(embed=embed)

    @uhc.command(name="match")
    async def match(self, ctx, id_):
        await ctx.channel.trigger_typing()
        data = await get(self.session, f"https://hosts.uhc.gg/api/matches/{id_}")
        if data:
            embed = discord.Embed(title=id, description=data["content"])
            embed.add_field(name="author", value=data["author"])
            embed.add_field(name="address", value=data["address"])
            embed.add_field(name="opens", value=data["opens"])
            embed.add_field(name="slots", value=data["slots"])
            embed.add_field(name="mainVersion", value=data["mainVersion"])
            embed.add_field(name="version", value=data["version"])
            embed.add_field(name="length", value=data["length"])
            embed.add_field(name="mapSize", value=data["mapSize"])
            embed.add_field(name="pvpEnabledAt", value=data["pvpEnabledAt"])
            embed.add_field(name="location", value=data["location"])
            embed.add_field(name="created", value=data["created"])
            embed.add_field(name="count", value=data["count"])
            embed.add_field(name="scenarios", value=data["scenarios"].join("\n"))
            embed.add_field(name="tags", value=data["tags"].join(" "))
        else:
            embed = discord.Embed(title=id, description="Match not found.")
        await ctx.send(embed=embed)

    @uhc.command(name="banned")
    async def uhc_banned(self, ctx, user):
        await ctx.channel.trigger_typing()
        try:
            UUID(user, version=4)
            uuid = user
        except ValueError:
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            uuid = await uuid_from_username(user, self.bot, self.session, ctx)
            uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

        data = await get(self.session, f"https://hosts.uhc.gg/api/ubl/{uuid}")
        if data:
            embed = discord.Embed(color=0x00FF00)
            for ban in data:
                value = (
                    f"Date: {ban['created']}\n"
                    f"Expires: {ban['expires']}\n"
                    f"Reason: {ban['reason']}\n"
                    f"Link: {ban['link']}\n"
                    f"Created by: {ban['createdBy']}"
                )
                embed.add_field(name=ban["id"], value=value)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No ban information for {uuid}")

    @commands.command()
    async def mcbug(self, ctx, bug=None):
        """ Gets info on a bug from bugs.mojang.com"""
        if bug:
            await ctx.channel.trigger_typing()
            data = await get(
                self.session, f"https://bugs.mojang.com/rest/api/latest/issue/{bug}"
            )
            if data:
                embed = discord.Embed(
                    description=data["fields"]["description"], color=0x00FF00,
                )

                embed.set_author(
                    name=f"{data['fields']['project']['name']} - {data['fields']['summary']}",
                    url=f"https://bugs.mojang.com/browse/{bug}",
                )

                info = (
                    f"Version: {data['fields']['project']['name']}\n"
                    f"Reporter: {data['fields']['creator']['displayName']}\n"
                    f"Created: {data['fields']['created']}\n"
                    f"Votes: {data['fields']['votes']['votes']}\n"
                    f"Updates: {data['fields']['updated']}\n"
                    f"Watchers: {data['fields']['watches']['watchCount']}"
                )

                details = (
                    f"Type: {data['fields']['issuetype']['name']}\n"
                    f"Status: {data['fields']['status']['name']}\n"
                )
                if data["fields"]["resolution"]["name"]:
                    details += f"Resolution: {data['fields']['resolution']['name']}\n"
                if "version" in data["fields"]:
                    details += f"Affected: { ', '.join(s['name'] for s in data['fields']['versions'])}\n"
                if "fixVersions" in data["fields"]:
                    if len(data["fields"]["fixVersions"]) >= 1:
                        details += f"Fixed Version: {data['fields']['fixVersions'][0]} + {len(data['fields']['fixVersions'])}\n"

                embed.add_field(name="Information", value=info)
                embed.add_field(name="Details", value=details)

                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    f"{ctx.message.author.mention},  :x: The bug {bug} was not found."
                )
        else:
            await ctx.send(f"{ctx.message.author.mention},  :x: Please provide a bug.")

    @commands.command()
    async def wiki(self, ctx, *, query):
        """Get an article from the minecraft wiki"""
        async with ctx.channel.typing():

            def generate_payload(query):
                """Generate the payload for Gamepedia based on a query string."""
                payload = {}
                payload["action"] = "query"
                payload["titles"] = query.replace(" ", "_")
                payload["format"] = "json"
                payload["formatversion"] = "2"  # Cleaner json results
                # Include extract in returned results
                payload["prop"] = "extracts"
                # Only return summary paragraph(s) before main content
                payload["exintro"] = "1"
                payload["redirects"] = "1"  # Follow redirects
                # Make sure it's plaintext (not HTML)
                payload["explaintext"] = "1"
                return payload

            base_url = "https://minecraft.gamepedia.com/api.php"
            footer_icon = (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Wikimedia-logo.png"
                "/600px-Wikimedia-logo.png"
            )

            payload = generate_payload(query)

            async with self.session.get(base_url, params=payload) as resp:
                result = await resp.json()

            try:
                # Get the last page. Usually this is the only page.
                page = result["query"]["pages"][-1]
                title = page["title"]
                description = page["extract"].strip().replace("\n", "\n\n")
                url = f"https://minecraft.gamepedia.com/{title.replace(' ', '_')}"

                if len(description) > 1500:
                    description = description[:1500].strip()
                    description += f"... [(read more)]({url})"

                embed = discord.Embed(
                    title=f"Minecraft Gamepedia: {title}",
                    description="\u2063\n{}\n\u2063".format(description),
                    color=0x00FF00,
                    url=url,
                )
                embed.set_footer(
                    text="Information provided by Wikimedia", icon_url=footer_icon
                )
                await ctx.send(embed=embed)

            except KeyError:
                await ctx.send(f"I'm sorry, I couldn't find \"{query}\" on Gamepedia")

    @commands.command()
    async def colorcodes(self, ctx, color=None):
        """get information on colour codes"""
        if color in colours:
            embed = discord.Embed(
                title=color, color=("%02x%02x%02x" % colours[color]["rgb"])
            )
            embed.add_field(
                name="Color Information",
                value=f"RGB: {colours[color]['rgb']}\nHEX: {'%02x%02x%02x' % colours[color]['rgb']}\n BACKGROUND-COLOR RGB: {colours[color]['background-rgb']}\nHEX: {'%02x%02x%02x' % colours[color]['background-rgb']}\n ",
            )

            embed.add_field(
                name="Text format code",
                value=f"To format text start it with `{colours[color]['code']}` and end it with `§r` eg `{colours[color]['code']}text§r`",
            )
