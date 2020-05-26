import discord
from discord.ext import commands
from utils.utils import uuid_from_username
import logging
import os.path
from random import choice

log = logging.getLogger(__name__)


class images(commands.Cog, name="Images"):
    def __init__(self, bot):
        self.session = bot.session
        self.bot = bot

    @commands.command(aliases=["ach", "advancement"])
    async def achievement(self, ctx, block_name, title, text):
        """Create your very own custom Minecraft achievements"""
        await ctx.channel.trigger_typing()
        embed = discord.Embed(color=0x00FF00)
        embed.set_image(
            url=f"https://api.bowie-co.nz/api/v1/images/advancement?item={block_name}&title={title}&text={text}"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def sign(self, ctx, line1, line2="%20", line3="%20", line4="%20"):
        """Create your very own custom Minecraft achievements"""
        await ctx.channel.trigger_typing()
        embed = discord.Embed(color=0x00FF00)
        embed.set_image(
            url=f"https://api.bowie-co.nz/api/v1/images/sign?line1={line1}&line2={line2}&line3={line3}&line4={line4}"
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
            await ctx.send("Painting not found")

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
        uuid, username = await uuid_from_username(username, self.session, self.bot, ctx)
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
        uuid, username = await uuid_from_username(username, self.session, self.bot, ctx)
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
        uuid, username = await uuid_from_username(username, self.session, self.bot, ctx)
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
    async def render(self, ctx, type_=None, username=None):
        """Renders a Minecraft players skin in 6 different ways. You can choose from these 6 render types: face, front, frontfull, head, bust & skin."""
        await ctx.channel.trigger_typing()
        renders = ["face", "front", "frontfull", "head", "bust", "skin"]
        if type_ in renders:
            uuid, username = await uuid_from_username(
                username, self.session, self.bot, ctx
            )
            if uuid:
                embed = discord.Embed(
                    description=f"Here is: `{username}`'s {type_}! \n **[DOWNLOAD](https://visage.surgeplay.com/{type_}/512/{uuid})**",
                    color=0x00FF00,
                )
                embed.set_image(url=f"https://visage.surgeplay.com/{type_}/512/{uuid}")

                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    f"{ctx.message.author.mention}, :x: The user: `{username}` does not exist!"
                )
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, Please supply a render type. Your options are:\n `face`, `front`, `frontfull`, `head`, `bust`, `skin` \n Type: ?render <render type> <username>"
            )
