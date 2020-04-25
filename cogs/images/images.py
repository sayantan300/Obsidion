import discord
from discord.ext import commands
from utils.utils import get_uuid, get
import logging
import os.path
from random import choice

log = logging.getLogger(__name__)


class images(commands.Cog, name="Images"):
    def __init__(self, bot):
        self.session = bot.session
        self.bot = bot

    @commands.command(aliases=["ach", "advancement"])
    async def achievement(self, ctx, block_id, title, word1, word2=None, word3=None):
        """Create your very own custom Minecraft achievements!
        
        Block IDS:
        stone: 1\ndiamond: 2\nsword: 3\ncreeper: 4\npig: 5\nTNT: 6\ncookie: 7\nheart: 8\nbed: 9\ncake: 10
        sign: 11\nrail: 12\ncrafting table: 13\nredstone: 14\nfire: 15\ncobweb: 16\nchest: 17\nfurnace: 18\nbook: 19\nstone: 20
        wooden plank: 21\niron: 22\ngold: 23\nwooden door: 24\niron door: 25\nchestplate: 26\nflint and steel: 27\npotion: 28\nsplash potion: 29\nspawn egg: 30
        coal: 31\niron sword: 32\nbow: 33\narrow: 34\niron chestplate: 35\nbucket: 36\nwater bucket: 37\nlava bucket: 38\nmilk bucket:39"""
        await ctx.channel.trigger_typing()
        embed = discord.Embed(color=0x00FF00)
        if word2 is None:
            embed.set_image(
                url=f"https://minecraftskinstealer.com/achievement/a.php?i={block_id}&h={title}&t={word1}"
            )
        elif word3 is None:
            embed.set_image(
                url=f"https://minecraftskinstealer.com/achievement/a.php?i={block_id}&h={title}&t={word1}+{word2}"
            )
        else:
            embed.set_image(
                url=f"https://minecraftskinstealer.com/achievement/a.php?i={block_id}&h={title}&t={word1}+{word2}+{word3}"
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def item(self, ctx, *, name):
        """view the image for a item"""
        name = name.replace(" ", "_").lower()
        if os.path.isfile(f"cogs/images/items/{name}.png"):
            file = discord.File(f"cogs/images/items/{name}.png", filename=f"{name}.png")
            embed = discord.Embed(title=name, color=0x00FF00)
            embed.set_image(url=f"attachment://{name}.png")
            await ctx.send(file=file, embed=embed)
        else:
            await ctx.send("Item not found")

    @commands.command()
    async def painting(self, ctx, name=None):
        """view the image for a item"""
        if not name:
            name = choice([f for f in os.listdir("cogs/images/painting")]).split(".")[0]
        if os.path.isfile(f"cogs/images/painting/{name}.png"):
            file = discord.File(
                f"cogs/images/painting/{name}.png", filename=f"{name}.png"
            )
            embed = discord.Embed(title=name, color=0x00FF00)
            embed.set_image(url=f"attachment://{name}.png")
            await ctx.send(file=file, embed=embed)
        else:
            await ctx.send("Item not found")

    @commands.command()
    async def effect(self, ctx, name=None):
        """view the image for a item"""
        if not name:
            name = choice([f for f in os.listdir("cogs/images/effect")]).split(".")[0]
        if os.path.isfile(f"cogs/images/effect/{name}.png"):
            file = discord.File(
                f"cogs/images/effect/{name}.png", filename=f"{name}.png"
            )
            embed = discord.Embed(title=name, color=0x00FF00)
            embed.set_image(url=f"attachment://{name}.png")
            await ctx.send(file=file, embed=embed)
        else:
            await ctx.send("Item not found")

    @commands.command()
    async def avatar(self, ctx, username=None):
        """Renders a Minecraft players face."""
        await ctx.channel.trigger_typing()
        if username:
            uuid = await get_uuid(self.session, username)
        if await self.bot.pool.fetchval(
            "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
        ):
            if await self.bot.pool.fetchval(
                "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
            ):
                uuid = await self.bot.pool.fetchval(
                    "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
                )
                names = await get(
                    self.session, f"https://api.mojang.com/user/profiles/{uuid}/names"
                )
                username = names[-1]["name"]
            else:
                uuid = False
        if uuid:
            embed = discord.Embed(
                description=f"Here is: `{username}`'s Face! \n **[DOWNLOAD](https://visage.surgeplay.com/face/512/{uuid})**",
                color=0x00FF00,
            )
            embed.set_image(url=f"https://visage.surgeplay.com/face/512/{uuid}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: The user: `{username}` does not exist!"
            )

    @commands.command()
    async def skull(self, ctx, username=None):
        """Renders a Minecraft players skull."""
        await ctx.channel.trigger_typing()
        if username:
            uuid = await get_uuid(self.session, username)
        elif await self.bot.pool.fetchval(
            "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
        ):
            uuid = await self.bot.pool.fetchval(
                "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
            )
            names = await get(
                self.session, f"https://api.mojang.com/user/profiles/{uuid}/names"
            )
            username = names[-1]["name"]
        if uuid:
            embed = discord.Embed(
                description=f"Here is: `{username}`'s Skull! \n **[DOWNLOAD](https://visage.surgeplay.com/head/512/{uuid})**",
                color=0x00FF00,
            )
            embed.set_image(url=f"https://visage.surgeplay.com/head/512/{uuid}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: The user: `{username}` does not exist!"
            )

    @commands.command()
    async def skin(self, ctx, username=None):
        """Renders a Minecraft players skin."""
        await ctx.channel.trigger_typing()
        if username:
            uuid = await get_uuid(self.session, username)
        elif await self.bot.pool.fetchval(
            "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
        ):
            uuid = await self.bot.pool.fetchval(
                "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
            )
            names = await get(
                self.session, f"https://api.mojang.com/user/profiles/{uuid}/names"
            )
            username = names[-1]["name"]
        if uuid:
            embed = discord.Embed(
                description=f"Here is: `{username}`'s Skin! \n **[DOWNLOAD](https://visage.surgeplay.com/full/512/{uuid})**",
                color=0x00FF00,
            )
            embed.set_image(url=f"https://visage.surgeplay.com/full/512/{uuid}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: The user: `{username}` does not exist!"
            )

    @commands.command()
    async def render(self, ctx, username=None, type=None):
        """Renders a Minecraft players skin in 6 different ways. You can choose from these 6 render types: face, front, frontfull, head, bust & skin."""
        await ctx.channel.trigger_typing()
        renders = ["face", "front", "frontfull", "head", "bust", "skin"]
        if type in renders:
            if username:
                uuid = await get_uuid(self.session, username)
            elif await self.bot.pool.fetchval(
                "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
            ):
                uuid = await self.bot.pool.fetchval(
                    "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
                )
                names = await get(
                    self.session, f"https://api.mojang.com/user/profiles/{uuid}/names"
                )
                username = names[-1]["name"]
            if uuid:
                embed = discord.Embed(
                    description=f"Here is: `{username}`'s {type}! \n **[DOWNLOAD](https://visage.surgeplay.com/{type}/512/{uuid})**",
                    color=0x00FF00,
                )
                embed.set_image(url=f"https://visage.surgeplay.com/{type}/512/{uuid}")

                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    f"{ctx.message.author.mention}, :x: The user: `{username}` does not exist!"
                )
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, Please supply a render type. Your options are:\n `face`, `front`, `frontfull`, `head`, `bust`, `skin` \n Type: ?render <username> <render type>"
            )
