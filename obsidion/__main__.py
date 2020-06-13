#!/usr/bin/env python

import logging

import discord
from discord.ext.commands import when_mentioned_or

# Set the event loop policies here so any subsequent `new_event_loop()`
# calls, in particular those as a result of the following imports,
# return the correct loop object.
from obsidion import __version__, _update_event_loop_policy, constants
from obsidion.bot import Obsidion

_update_event_loop_policy()


log = logging.getLogger("obsidion.main")

# set activity
activity = discord.Activity(
    name=constants.Bot.status, type=discord.ActivityType.watching,
)

bot = Obsidion(
    case_insensitive=True,
    activity=activity,
    command_prefix=when_mentioned_or(constants.Bot.default_prefix),
)

# Load all required cogs

# core cogs
bot.load_extension("obsidion.core.development")
bot.load_extension("obsidion.core.help")
bot.load_extension("obsidion.core.error_handler")

# extensions and main features
bot.load_extension("obsidion.cogs.misc")
bot.load_extension("obsidion.cogs.redstone")
bot.load_extension("obsidion.cogs.fun")
bot.load_extension("obsidion.cogs.info")
bot.load_extension("obsidion.cogs.images")
bot.load_extension("obsidion.cogs.hypixel")

# TODO
# bot.load_extension("obsidion.cogs.config")
# bot.load_extension("obsidion.cogs.servers")

# run bot
bot.run(constants.Bot.discord_token)
