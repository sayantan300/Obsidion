import logging

from obsidion.utils.utils import get
from obsidion import constants

import discord
from discord.ext import commands

log = logging.getLogger(__name__)


class info(commands.Cog):
    """commands that are bot related."""

    def __init__(self, bot):
        """initialise the bot"""
        self.bot = bot
        self.session = bot.http_session

    @commands.group(aliases=["uhcgg", "uhc.gg"])
    async def uhc(self, ctx: commands.Context):
        """View info about uhc matches."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @uhc.command(name="upcoming")
    async def uhc_upcoming(self, ctx: commands.Context):
        """View upcoming Matches on uhc.gg."""
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
            _id = match["id"]

            info = ""
            info += f"Opens: {opens}\n"
            info += f"Author: {author}\n"
            info += f"Region: {region}\n"
            info += f"Version: {version}\n"
            info += f"Slots: {slots}\n"
            info += f"Length: {length} minutes\n"
            info += f"Tournament: {tournament}\n"
            info += f"id: {_id}"

            embed.add_field(name=address, value=info)

        await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx: commands.Context):
        """Check the status of all the Mojang services"""
        await ctx.channel.trigger_typing()
        data = await get(self.session, f"{constants.Bot.api}/mojang/check")
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
    async def sales(self, ctx: commands.Context):
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

        if not sales_data:
            ctx.send(
                f"{ctx.author}, :x: the Mojang API is not currently available please try again soon"
            )
            return
        embed = discord.Embed(color=0x00FF00)

        sale = (
            f"Total Sales: `{sales_data['total']:,}`\n"
            f"Sales in the last 24 hours: `{sales_data['last24h']:,}`\n"
            f"Sales per second: `{sales_data['saleVelocityPerSeconds']}`\n"
            "[BUY MINECRAFT](https://my.minecraft.net/en-us/store/minecraft/)"
        )

        embed.add_field(name="Minecraft Sales", value=sale)

        await ctx.send(embed=embed)

    @commands.command()
    async def mcbug(self, ctx: commands.Context, bug: str = None):
        """Gets info on a bug from bugs.mojang.com."""
        if not bug:
            await ctx.send(f"{ctx.message.author.mention},  :x: Please provide a bug.")
            return
        await ctx.channel.trigger_typing()
        data = await get(
            self.session, f"https://bugs.mojang.com/rest/api/latest/issue/{bug}"
        )
        if not data:
            await ctx.send(
                f"{ctx.message.author.mention},  :x: The bug {bug} was not found."
            )
            return
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

    @commands.command()
    async def wiki(self, ctx: commands.Context, *, query: str):
        """Get an article from the minecraft wiki"""
        await ctx.channel.trigger_typing()

        def generate_payload(query):
            """Generate the payload for Gamepedia based on a query string."""
            payload = {
                "action": "query",
                "titles": query.replace(" ", "_"),
                "format": "json",
                "formatversion": "2",  # Cleaner json results
                "prop": "extracts",  # Include extract in returned results
                "exintro": "1",  # Only return summary paragraph(s) before main content
                "redirects": "1",  # Follow redirects
                "explaintext": "1",  # Make sure it's plaintext (not HTML)
            }
            return payload

        base_url = "https://minecraft.gamepedia.com/api.php"
        footer_icon = (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Wikimedia-logo.png"
            "/600px-Wikimedia-logo.png"
        )

        payload = generate_payload(query)

        result = await get(self.session, base_url, payload)

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
                description=f"\u2063\n{description}\n\u2063",
                color=0x00FF00,
                url=url,
            )
            embed.set_footer(
                text="Information provided by Wikimedia", icon_url=footer_icon
            )
            await ctx.send(embed=embed)

        except KeyError:
            await ctx.send(f"I'm sorry, I couldn't find \"{query}\" on Gamepedia")
