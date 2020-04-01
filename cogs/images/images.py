import discord
from discord.ext import commands
from utils.utils import get_uuid

class images(commands.Cog, name="Images"):

    def __init__(self, bot):
        self.session = bot.session

    @commands.command()
    async def achievement(self, ctx, block_id=None, title=None, word1=None, word2=None, word3=None):
        """Create your very own custom Minecraft achievements!"""
        if title and word1 and block_id:
            embed = discord.Embed(color=0x00ff00)
            if word2 == None:
                embed.set_image(url=f"https://minecraftskinstealer.com/achievement/a.php?i={block_id}&h={title}&t={word1}")
            elif word3 == None:
                embed.set_image(url=f"https://minecraftskinstealer.com/achievement/a.php?i={block_id}&h={title}&t={word1}+{word2}")
            else:
                embed.set_image(url=f"https://minecraftskinstealer.com/achievement/a.php?i={block_id}&h={title}&t={word1}+{word2}+{word3}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: Please supply a block_id title and 1-3 words")
    
    @commands.command()
    async def avatar(self, ctx, username):
        """Renders a Minecraft players face."""
        uuid = await get_uuid(self.session, username)
        if uuid:
            embed = discord.Embed(description=f"Here is: `{username}`'s Face! \n **[DOWNLOAD SKIN](https://visage.surgeplay.com/skin/{uuid})**", color=0x00ff00)
            embed.set_image(url=f"https://visage.surgeplay.com/face/{uuid}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: The user: `{username}` does not exist!")

    
    @commands.command()
    async def skull(self, ctx, username):
        """Renders a Minecraft players skull."""
        uuid = await get_uuid(self.session, username)
        if uuid:
            embed = discord.Embed(description=f"Here is: `{username}`'s Skull! \n **[DOWNLOAD SKIN](https://visage.surgeplay.com/skin/{uuid})**", color=0x00ff00)
            embed.set_image(url=f"https://visage.surgeplay.com/head/{uuid}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: The user: `{username}` does not exist!")

    
    @commands.command()
    async def skin(self, ctx, username):
        """Renders a Minecraft players skin."""
        uuid = await get_uuid(self.session, username)
        if uuid:
            embed = discord.Embed(description=f"Here is: `{username}`'s Skin! \n **[DOWNLOAD SKIN](https://visage.surgeplay.com/skin/{uuid})**", color=0x00ff00)
            embed.set_image(url=f"https://visage.surgeplay.com/full/{uuid}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.message.author.mention}, :x: The user: `{username}` does not exist!")

    @commands.command()
    async def render(self, ctx, username, type):
        """Renders a Minecraft players skin in 6 different ways. You can choose from these 6 render types: face, front, frontfull, head, bust & skin."""
        renders = ["face", "front", "frontfull", "head", "bust", "skin"]
        if type in renders:
            uuid = await get_uuid(self.session, username)
            if uuid:
                embed = discord.Embed(description=f"Here is: `{username}`'s {type}! \n **[DOWNLOAD SKIN](https://visage.surgeplay.com/skin/{uuid})**", color=0x00ff00)
                embed.set_image(url=f"https://visage.surgeplay.com/{type}/{uuid}")

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{ctx.message.author.mention}, :x: The user: `{username}` does not exist!")
        else:
            await ctx.send(f"{ctx.message.author.mention}, Please supply a render type. Your options are:\n `face`, `front`, `frontfull`, `head`, `bust`, `skin` \n Type: ?render <username> <render type>")