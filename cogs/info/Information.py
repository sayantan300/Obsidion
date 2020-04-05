from discord.ext import commands
from random import choice
import discord
import aiohttp
from datetime import datetime
import json
from utils.utils import get, get_uuid
from uuid import UUID
from mcstatus import MinecraftServer
from py_mcpe_stats import Query
import base64
import io


class Information(commands.Cog, name="Information"):

    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @commands.command(aliases=['whois', 'p', "names", "namehistory", "pastnames", "namehis"])
    async def profile(self, ctx, username=None):
        """View a players Minecraft UUID, Username history and skin."""
        await ctx.channel.trigger_typing()
        if username:
            uuid = await get_uuid(self.session, username)
        elif str(ctx.author.id) in self.bot.pool["user"]:
            if self.bot.pool["user"][str(ctx.author.id)]["uuid"]:
                uuid = self.bot.pool["user"][str(ctx.author.id)]["uuid"]
                names = await get(self.session, f"https://api.mojang.com/user/profiles/{uuid}/names")
                username = names[-1]["name"]
            else:
                uuid = False
        else:
            uuid = False

        if uuid:
            long_uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

            names = await get(self.session, f"https://api.mojang.com/user/profiles/{uuid}/names")

            name_list = ""
            for name in names[::-1][:-1]:
                name1 = name["name"]
                date = datetime.utcfromtimestamp(
                    int(str(name["changedToAt"])[:-3])).strftime('%b %d, %Y')
                name_list += f"**{names.index(name)+1}.** `{name1}` - {date} " + "\n"
            original = names[0]["name"]
            name_list += f"**1.** `{original}` - First Username"

            uuids = "Short UUID: `" + uuid + "\n" + "`Long UUID: `" + long_uuid + "`"
            information = ""
            information += f"Username Changes: `{len(names)-1}`\n"
            # information += f"Legacy: `{}`"

            embed = discord.Embed(
                title=f"Minecraft profile for {username}", color=0x00ff00)

            embed.add_field(name="UUID's", inline=False, value=uuids)
            embed.add_field(name="Textures", inline=True,
                            value=f"Skin: [Open Skin](https://visage.surgeplay.com/bust/{uuid})")
            embed.add_field(name="Information", inline=True,
                            value=information)
            embed.add_field(name="Name History", inline=False, value=name_list)
            embed.set_thumbnail(
                url=(f"https://visage.surgeplay.com/bust/{uuid}"))

            await ctx.send(embed=embed)
        else:
            await ctx.send("That username is not been used.")

    @commands.command(aliases=["available", "availability", "namecheck"])
    async def checkname(self, ctx, username):
        """Check weather a username is currently in use."""
        await ctx.channel.trigger_typing()
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
    async def uuid(self, ctx, username=None):
        """Get a players UUID."""
        await ctx.channel.trigger_typing()
        if username:
            uuid = await get_uuid(self.session, username)
        elif self.bot.pool["user"][str(ctx.author.id)]["uuid"]:
            uuid = self.bot.pool["user"][str(ctx.author.id)]["uuid"]
            names = await get(self.session, f"https://api.mojang.com/user/profiles/{uuid}/names")
            username = names[-1]["name"]
        else:
            uuid = False
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
    async def server(self, ctx, server=None):
        """
        Request a JAVA Minecraft server for information such as online player count, MOTD and more.

        :param server: This is for the url and port for the Minecraft java server in this format: `example.com:25565`
        """
        await ctx.channel.trigger_typing()
        if server:
            try:
                mc_server = MinecraftServer.lookup(server)
                data = mc_server.status()
            except:
                data = False
        elif self.bot.pool["guilds"][str(ctx.guild.id)]["server"]:
            server = self.bot.pool["guilds"][str(ctx.guild.id)]["server"]
            try:
                mc_server = MinecraftServer.lookup(server)
                data = mc_server.status()
            except:
                data = False

        if server:
            if data:
                embed = discord.Embed(
                    title=f"Java Server: {server}", color=0x00ff00)
                # need to fix encoding issues
                if 'text' in data.description:
                    embed.add_field(name="Description", value=data.description['text'])
                else:
                    embed.add_field(name="Description", value=data.description)

                embed.add_field(
                    name="Players", value=f"Online: `{data.players.online:,}` \n Maximum: `{data.players.max:,}`")
                if data.players.online > 10 or data.players.online == 0:
                    pass
                else:
                    names = "\n".join(data.players.names)
                    embed.add_field(name="Player names", value=names)

                embed.add_field(
                    name="Version", value=f"Java Edition \n Running: `{data.version.name}` \n Protocol: `{data.version.protocol}`", inline=False)
                
                encoded = base64.decodebytes(data.favicon[22:].encode('utf-8'))
                image_bytesio = io.BytesIO(encoded)
                thumb = discord.File(image_bytesio, 'thumb.png')
                embed.set_thumbnail(url='attachment://thumb.png')
                
                await ctx.send(embed=embed, file=thumb)
            else:
                await ctx.send("The server is currently offline")
        else:
            if server:
                await ctx.send(f"{ctx.author}, :x: The Jave edition Minecraft server `{server}` is currently not online or cannot be requested")
            else:
                await ctx.send(f"{ctx.author}, :x: Please provide a server")

    @commands.command()
    async def serverpe(self, ctx, server=None):
        """Get information about a Bedrock Edition Server"""
        if server:
            host, port = server.split(":")

            q = Query(host, int(port))
            server_data = q.query()
            print(vars(server_data))

            if server_data:
                embed = discord.Embed(
                        title=f"Bedrock Server: {server}", color=0x00ff00)

                embed.add_field(name="Description", value=server_data.SERVER_NAME, inline=False)
                embed.add_field(name="Players", value=f"Online: `{server_data.NUM_PLAYERS}`\nMax: `{server_data.MAX_PLAYERS}`")
                embed.add_field(name="Version", value=f"Bedrock Edition\nRunning: `{server_data.GAME_VERSION}`")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{ctx.author}, :x: The Bedrock edition Minecraft server `{server}` is currently not online or cannot be requested")
        else:
            await ctx.send(f"{ctx.author}, :x: Please provide a server")

    # This has been temporarily disabled due to Mojangs API not updateding
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # @commands.command()
    # async def status(self, ctx):
    #    """Check the status of all the Mojang services"""
    #    await ctx.channel.trigger_typing()
    #    data = await get(self.session, "https://status.mojang.com/check")

    #    sales_mapping = {
    #        'item_sold_minecraft': True,
    #        'prepaid_card_redeemed_minecraft': True,
    #        'item_sold_cobalt': False,
    #        'item_sold_scrolls': False
    #    }
    #    payload = {
    #        'metricKeys': [k for (k, v) in sales_mapping.items() if v]
    #    }

    #    url = "https://api.mojang.com/orders/statistics"
    #    async with self.session.post(url, json=payload) as resp:
    #        if resp.status == 200:
    #            sales_data = await resp.json()

    #    embed = discord.Embed(
    #        title=f"Minecraft Service Status", color=0x00ff00)
    #    embed.add_field(name="Minecraft Game Sales",
    #                    value=f"Total Sales: **{sales_data['total']:,}** Last 24 Hours: **{sales_data['last24h']:,}**")

    #    services = ""
    #    for service in data:
    #        if service[next(iter(service))] == "green":
    #            services += f":green_heart: - {next(iter(service)).title()}: **This service is healthy.** \n"
    #        elif service[next(iter(service))] == "yellow":
    #            services += f":yellow_heart: - {next(iter(service)).title()}: **This service has some issues.** \n"
    #        else:
    #            services += f":heart: - {next(iter(service)).title()}: **This service is offline.** \n"
    #    embed.add_field(name="Minecraft Services:",
    #                    value=services, inline=False)

    #    await ctx.send(embed=embed)

    @commands.command()
    async def sales(self, ctx):
        """See the total sales of Minecraft"""
        await ctx.channel.trigger_typing()
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
                prefix = self.bot.pool["guilds"][str(ctx.guild.id)]["prefix"]
            embed = discord.Embed(title="Command Usage", description=f"`{prefix}uhc upcoming` - Shows 6 upcoming matches.\n`{prefix}uhc banned <uuid | username>` - View the bans of a player.", color=0x00ff00)
            await ctx.send(embed=embed)
    
    @uhc.command(name="upcoming")
    async def uhc_upcoming(self, ctx):
        await ctx.channel.trigger_typing()
        data = await get(self.session, "https://hosts.uhc.gg/api/matches/upcoming")

        embed = discord.Embed(title="UHC.gg upcoming UHC games",
                                description="Displayed the top 6 upcoming UHC games on [hosts.uhc.gg](https://hosts.uhc.gg)\n", color=0x00ff00)

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
    
    @uhc.command(name="match")
    async def match(self, ctx, param):
        pass

    @uhc.command(name="banned")
    async def uhc_banned(self, ctx, user):
        await ctx.channel.trigger_typing()
        try:
            val = UUID(user, version=4)
            uuid = user
        except ValueError:
            # If it's a value error, then the string 
            # is not a valid hex code for a UUID.
            uuid = await get_uuid(self.session, user)
            uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

        data = await get(self.session, f"https://hosts.uhc.gg/api/ubl/{uuid}")
        if data:
            embed = discord.Embed(color=0x00ff00)
            for ban in data:
                value = ""
                value += f"Date: {ban['created']}\n"
                value += f"Expires: {ban['expires']}\n"
                value += f"Reason: {ban['reason']}\n"
                value += f"Link: {ban['link']}\n"
                value += f"Created by: {ban['createdBy']}"
                embed.add_field(name=ban["id"], value=value)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No ban information for {uuid}")


    @commands.command(aliases=["bug"])
    async def mcbug(self, ctx, bug=None):
        """ Gets info on a bug from bugs.mojang.com"""
        if bug:
            await ctx.channel.trigger_typing()
            data = await get(self.session, f"https://bugs.mojang.com/rest/api/latest/issue/{bug}")
            if data:
                embed = discord.Embed(title=f"[{data['fields']['project']['name']} - {data['fields']['summary']}](https://bugs.mojang.com/rest/api/latest/issue/{bug})",
                                      description=data["fields"]["description"], color=0x00ff00)

                info = ""
                info += f"Version: {data['fields']['project']['name']}\n"
                info += f"Reporter: {data['fields']['creator']['displayName']}\n"
                info += f"Created: {data['fields']['created']}\n"
                info += f"Votes: {data['fields']['votes']['votes']}\n"
                info += f"Updates: {data['fields']['updated']}\n"
                info += f"Watchers: {data['fields']['watches']['watchCount']}"

                details = ""
                details += f"Type: {data['fields']['issuetype']['name']}\n"
                details += f"Status: {data['fields']['status']['name']}\n"
                details += f"Resolution: {data['fields']['resolution']['name']}\n"
                details += f"Affected: { ', '.join([s['name'] for s in data['fields']['versions']])}\n"
                if len(data['fields']['fixVersions']) >= 1:
                    details += f"Fixed Version: {data['fields']['fixVersions'][0]} + {len(data['fields']['fixVersions'])}\n"

                embed.add_field(name="Information", value=info)
                embed.add_field(name="details", value=details)

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{ctx.message.author.mention},  :x: The bug {bug} was not found.")
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
                    description=u"\u2063\n{}\n\u2063".format(description),
                    color=0x00ff00,
                    url=url,
                )
                embed.set_footer(
                    text="Information provided by Wikimedia", icon_url=footer_icon
                )
                await ctx.send(embed=embed)

            except KeyError:
                await ctx.send(f"I'm sorry, I couldn't find \"{query}\" on Gamepedia")

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
