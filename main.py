import discord
from discord.ext import commands

import sys
import traceback
import json


def token():
    # load token from json file
    with open("config.json", "r") as f:
        setup = json.load(f)
    return setup["setup"]["token"]


def get_prefix(guild_id, message):
    # get custotm prefect per server
    with open("data.json", "r+") as f:
        json_data = json.load(f)
    try:
        return json_data["server"][str(message.guild.id)]
    except:
        print("error")
        with open("data.json", "r+") as f:
            json_data = json.load(f)
            json_data["server"][str(message.guild.id)] = "/"
            f.seek(0)
            json.dump(json_data, f, indent=4)
            f.truncate()
        return "/"


def extensions():
    with open("config.json", "r") as f:
        json_data = json.load(f)
    cogs = json_data["setup"]["cogs"]
    return cogs


bot = commands.Bot(command_prefix=get_prefix, description="Testing", case_insensitive=True)

@bot.event
async def on_ready():
    print(f"\n\nSuccessfully logged in and booted...!")
    print(f"Logged in as: {bot.user.name} - {bot.user.id}")
    print(f"Invite link: https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot")
    print(f"Version: {discord.__version__}\n")

    # Sets our bots status to wether operational or testing
    game = discord.Game("Testing")
    await bot.change_presence(status=discord.Status.online, activity=game)

if __name__ == "__main__":
    # remove default help command so we can use our own
    bot.remove_command('help')

    # load all the cogs
    for extension in extensions():
        try:
            bot.load_extension(f"cogs.{extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()

bot.run(token(), bot=True, reconnect=True)
