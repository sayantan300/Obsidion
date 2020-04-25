from discord.ext import tasks, commands
from mcstatus import MinecraftServer
import discord
from random import choice
import config
from utils.utils import load_from_text


class loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servert_task.start()

    def cog_unload(self):
        self.servert_task.cancel()

    @tasks.loop(minutes=5)
    async def servert_task(self):
        for channel, server in await self.bot.pool.fetch(
            "SELECT channel, server FROM servertracking"
        ):
            # loop through every minecraft server
            try:
                mc_server = MinecraftServer.lookup(server)
                data = mc_server.status()
            except:
                data = False
            channel = self.bot.get_channel(channel)
            # check
            if data:
                name = f"{server.split('.')[-2].title()}: {data.players.online:,} / {data.players.max:,}"
                await channel.edit(name=name)
            else:
                await channel.edit(name="SERVER IS OFFLINE")

    @servert_task.before_loop
    async def before_servert_task(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.bot.pool.fetchval(
            "SELECT server_join from guild WHERE id = $1", member.guild.id
        ):
            join = load_from_text("join")
            channel = await self.bot.pool.fetchval(
                "SELECT server_join from guild WHERE id = $1", member.guild.id
            )
            send_channel = self.bot.get_channel(channel)
            await send_channel.send(choice(join).replace("member", member.mention))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if config.new_guild_channel:
            users = sum(1 for m in guild.members if not m.bot)
            bots = sum(1 for m in guild.members if m.bot)
            members = f"Humans: `{users}/{len(guild.members)}` \n Bots: `{bots}/{len(guild.members)}`"

            if await self.bot.pool.fetch("SELECT * FROM guild WHERE id = $1", guild.id):
                embed = discord.Embed(
                    name=f"{self.bot.user.name} has re-joined a guild"
                )
                embed.set_footer(
                    text=f"Guild: {len(self.bot.guilds):,} | Shard: {guild.shard_id}/{self.bot.shard_count-1} | rejoin"
                )
            else:
                embed = discord.Embed(
                    name=f"{self.bot.user.name} has joined a new guild"
                )
                embed.set_footer(
                    text=f"Guild: {len(self.bot.guilds):,} | Shard: {guild.shard_id}/{self.bot.shard_count-1} | join"
                )
                await self.bot.pool.execute(
                    "INSERT INTO guild (id, prefix, serverTrack, server_join, silent) VALUES ($1, $2, $3, $4, $5)",
                    guild.id,
                    "/",
                    None,
                    None,
                    False,
                )
            embed.add_field(name="Name", value=f"`{guild.name}`")
            embed.add_field(name="Members", value=members)
            embed.add_field(name="Owner", value=guild.owner)
            embed.add_field(name="Region", value=guild.region, inline=False)
            if guild.icon_url:
                embed.set_thumbnail(url=guild.icon_url)
            else:
                embed.set_thumbnail(url="https://i.imgur.com/AFABgjD.png")
            channel = self.bot.get_channel(config.new_guild_channel)
            await channel.send(embed=embed)
