import logging

import discord
from discord.ext import commands

from obsidion import constants
from obsidion.bot import Obsidion

log = logging.getLogger(__name__)


class MyHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "help": "Shows help about the bot, a command, or a category",
                "hidden": True,
            }
        )


    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"[{command.name}|{aliases}]"
            if parent:
                fmt = f"{parent} {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{alias} {command.signature}"

    async def send_bot_help(self, mapping):
        bot = self.context.bot
        embed = discord.Embed(
            title="Bot support",
            description=f"Below is a list of commands you can use",
            colour=0x00FF00,
        )
        embed.set_footer(
            text=f'Type {self.context.prefix}help <command> for more info on a command. You can also type {self.context.prefix}help <category> for more info on a category.'
        )

        for cog in bot.cogs:
            cog_commands = bot.get_cog(cog).get_commands()
            if self.context.author in bot.owner_ids:
                # allow owner to see all the commands
                cogs = [c.name for c in cog_commands]
            else:
                cogs = [c.name for c in cog_commands if not c.hidden]

            if len(cogs) > 0:
                embed.add_field(name=cog, value=f"`{'`, `'.join(cogs)}`", inline=False)

        embed.add_field(
            inline=False,
            name="Support",
            value=f"**[ADD TO SERVER](https://discordapp.com/oauth2/authorize?client_id={constants.Bot.clientid}&scope=bot&permissions=314448) | [SUPPORT SERVER](https://discord.gg/invite/7BRD7s6)** | **[GITHUB](https://github.com/Darkflame72/Obsidion/)** | **[WEBSITE](http://obsidion.bowie-co.nz)** | **[PATREON](https://www.patreon.com/obsidion)**",
        )
        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f"{cog.qualified_name} Help",
            description="Below is a list of all the commands and their desriptions that belong to this module.",
            colour=0x00FF00,
        )
        embed.set_footer(
            text=f'Use "{self.context.prefix}help command" for more info on a command.'
        )

        cog_commands = cog.get_commands()
        command_list = [(c.name, c.help, c.hidden) for c in cog_commands]

        for command in command_list:
            if command[2] and self.context.author in self.context.bot.owner_ids:
                # allows owner to view commands that are not normally visible
                embed.add_field(name=command[0], value=f"`{command[1]}`", inline=False)
            elif not command[2]:
                embed.add_field(name=command[0], value=f"`{command[1]}`", inline=False)

        embed.add_field(
            inline=False,
            name="Support",
            value=f"**[ADD TO SERVER](https://discordapp.com/oauth2/authorize?client_id={constants.Bot.clientid}&scope=bot&permissions=314448) | [SUPPORT SERVER](https://discord.gg/invite/7BRD7s6)** | **[GITHUB](https://github.com/Darkflame72/Obsidion/)** | **[WEBSITE](http://obsidion.bowie-co.nz)** | **[PATREON](https://www.patreon.com/obsidion)**",
        )
        embed.set_footer(
            text=f'Type {self.context.prefix}help <command> for more info on a command. You can also type {self.context.prefix}help <category> for more info on a category.'
        )
        await self.context.send(embed=embed)

    def common_command_formatting(self, page_or_embed: discord.Embed, command):
        # page_or_embed.author = "Obsidion Help Menu"
        _help = f"`Syntax: {self.context.prefix}{command.qualified_name} {command.signature}`"
        if command.description:
            page_or_embed.description = _help
        else:
            page_or_embed.description = _help or "No help found..."

    async def send_command_help(self, command):
        embed = discord.Embed(colour=0x00FF00)

        self.common_command_formatting(embed, command)
        if len(command.aliases) > 0:
            embed.add_field(
                name=command.name,
                value=f"""
            Name: `{command.name}`
            Aliases: `{', '.join(command.aliases)}`
            Category: `{command.cog_name}`""",
            )
        else:
            embed.add_field(
                name=command.name,
                value=f"""
            Name: `{command.name}`
            Category: `{command.cog_name}`""",
            )
        embed.set_footer(
            text=f'Type {self.context.prefix}help <command> for more info on a command. You can also type {self.context.prefix}help <category> for more info on a category.'
        )
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(colour=0x00FF00)

        self.common_command_formatting(embed, group)

        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)

        sub = ""
        for entry in entries:
            sub += f"`{self.context.prefix}{group.name} {entry.name}` {entry.help}.\n"
        embed.add_field(name="Sub Commands:", value=sub)

        embed.add_field(
            name="Usage",
            value=f"`{self.context.prefix}{self.get_command_signature(group)}`",
            inline=False,
        )
        if len(group.aliases) > 0:
            embed.add_field(
                name=group.name,
                value=f"""
            Name: `{group.name}`
            Aliases: `{', '.join(group.aliases)}`
            Category: `{group.cog_name}`""",
            )
        else:
            embed.add_field(
                name=group.name,
                value=f"""
            Name: `{group.name}`
            Category: `{group.cog_name}`""",
            )
        embed.set_footer(
            text=f'Type {self.context.prefix}help <command> for more info on a command. You can also type {self.context.prefix}help <category> for more info on a category.'
        )

        await self.context.send(embed=embed)


class Help(commands.Cog):
    """Custom Embed Pagination Help feature."""

    def __init__(self, bot: Obsidion) -> None:
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self
        self.bot = bot

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot) -> None:
    """Load the Help cog."""
    bot.add_cog(Help(bot))
    log.info("Cog loaded: Help")
