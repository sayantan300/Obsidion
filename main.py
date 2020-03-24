import discord
from discord.ext import commands

import sys
import traceback
import json


def token():
    with open("data.json", "r") as f:
        setup = json.load(f)
    return setup["setup"]["token"]


def get_prefix(guild_id, message):
    with open("data.json", "r+") as f:
        json_data = json.load(f)
    try:
        return json_data["server"][str(message.guild.id)]["prefix"]
    except:
        with open("data.json", "r+") as f:
            json_data = json.load(f)
            json_data[str(message.guild.id)] = {"prefix": "/"}
            f.seek(0)
            json.dump(json_data, f, indent=4)
            f.truncate()
        return "/"


def extensions():
    with open("data.json", "r") as f:
        json_data = json.load(f)
    cogs = json_data["setup"]["cogs"]
    return cogs


bot = commands.Bot(command_prefix="?", description="Testing")

if __name__ == "__main__":
    for extension in extensions():
        try:
            bot.load_extension(f"cogs.{extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():

    print(f"\n\nSuccessfully logged in and booted...!")
    print(
        f"Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n")

    # Sets our bots status to wether operational or testing
    game = discord.Game("Testing")
    await bot.change_presence(status=discord.Status.online, activity=game)

bot.run(token(), bot=True, reconnect=True)
