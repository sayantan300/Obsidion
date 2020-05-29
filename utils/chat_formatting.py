import itertools
import datetime
from typing import Sequence, Iterator, List, Optional, Union, SupportsInt
from io import BytesIO

import discord


def error(text: str) -> str:
    return f"\N{NO ENTRY SIGN} {text}"


def warning(text: str) -> str:
    return f"\N{WARNING SIGN} {text}"


def info(text: str) -> str:
    return f"\N{INFORMATION SOURCE} {text}"


def question(text: str) -> str:
    return f"\N{BLACK QUESTION MARK ORNAMENT} {text}"


def bold(text: str, escape_formatting: bool = True) -> str:
    text = escape(text, formatting=escape_formatting)
    return f"**{text}**"


def box(text: str, lang: str = "") -> str:
    """Get the given text in a code block."""
    ret = f"```{lang}\n{text}\n```"
    return ret


def inline(text: str) -> str:
    """Get the given text as inline code."""
    if "`" in text:
        return f"``{text}``"
    else:
        return f"`{text}`"


def italics(text: str, escape_formatting: bool = True) -> str:
    """Get the given text in italics."""
    text = escape(text, formatting=escape_formatting)
    return f"*{text}*"


def underline(text: str, escape_formatting: bool = True) -> str:
    """Get the given text with an underline."""
    text = escape(text, formatting=escape_formatting)
    return f"__{text}__"


def strikethrough(text: str, escape_formatting: bool = True) -> str:
    """Get the given text with a strikethrough.
    Note: By default, this function will escape ``text`` prior to applying a strikethrough.
    """
    text = escape(text, formatting=escape_formatting)
    return f"~~{text}~~"


def escape(text: str, *, mass_mentions: bool = False, formatting: bool = False) -> str:
    """Get text with all mass mentions or markdown escaped."""
    if mass_mentions:
        text = text.replace("@everyone", "@\u200beveryone")
        text = text.replace("@here", "@\u200bhere")
    if formatting:
        text = discord.utils.escape_markdown(text)
    return text


def pagify(
    text: str,
    delims: Sequence[str] = ["\n"],
    *,
    priority: bool = False,
    escape_mass_mentions: bool = True,
    shorten_by: int = 8,
    page_length: int = 2000,
) -> Iterator[str]:
    """Generate multiple pages from the given text.
    Note
    ----
    This does not respect code blocks or inline code.
    Parameters
    """
    in_text = text
    page_length -= shorten_by
    while len(in_text) > page_length:
        this_page_len = page_length
        if escape_mass_mentions:
            this_page_len -= in_text.count("@here", 0, page_length) + in_text.count(
                "@everyone", 0, page_length
            )
        closest_delim = (in_text.rfind(d, 1, this_page_len) for d in delims)
        if priority:
            closest_delim = next((x for x in closest_delim if x > 0), -1)
        else:
            closest_delim = max(closest_delim)
        closest_delim = closest_delim if closest_delim != -1 else this_page_len
        if escape_mass_mentions:
            to_send = escape(in_text[:closest_delim], mass_mentions=True)
        else:
            to_send = in_text[:closest_delim]
        if len(to_send.strip()) > 0:
            yield to_send
        in_text = in_text[closest_delim:]

    if len(in_text.strip()) > 0:
        if escape_mass_mentions:
            yield escape(in_text, mass_mentions=True)
        else:
            yield in_text


def humanize_list(items: Sequence[str]) -> str:
    """Get comma-separted list, with the last element joined with *and*.
    This uses an Oxford comma, because without one, items containing
    the word *and* would make the output difficult to interpret."""
    if len(items) == 1:
        return items[0]
    try:
        return ", ".join(items[:-1]) + ", and " + items[-1]
    except IndexError:
        raise IndexError("Cannot humanize empty sequence") from None


def format_perms_list(perms: discord.Permissions) -> str:
    """Format a list of permission names.
    This will return a humanized list of the names of all enabled
    permissions in the provided `discord.Permissions` object."""
    perm_names: List[str] = []
    for perm, value in perms:
        if value is True:
            perm_name = '"' + perm.replace("_", " ").title() + '"'
            perm_names.append(perm_name)
    return humanize_list(perm_names).replace("Guild", "Server")


def humanize_timedelta(
    *,
    timedelta: Optional[datetime.timedelta] = None,
    seconds: Optional[SupportsInt] = None,
) -> str:
    """
    Get a locale aware human timedelta representation.
    This works with either a timedelta object or a number of seconds.
    Fractional values will be omitted, and values less than 1 second
    an empty string.
    """

    try:
        obj = seconds if seconds is not None else timedelta.total_seconds()
    except AttributeError:
        raise ValueError("You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        ("year", "years", 60 * 60 * 24 * 365),
        ("month", "months", 60 * 60 * 24 * 30),
        ("day", "days", 60 * 60 * 24),
        ("hour", "hours", 60 * 60),
        ("minute", "minutes", 60),
        ("second", "seconds", 1),
    ]

    strings = []
    for period_name, plural_period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 0:
                continue
            unit = plural_period_name if period_value > 1 else period_name
            strings.append(f"{period_value} {unit}")

    return ", ".join(strings)


def text_to_file(
    text: str,
    filename: str = "file.txt",
    *,
    spoiler: bool = False,
    encoding: str = "utf-8",
):
    """Prepares text to be sent as a file on Discord, without character limit.
    This writes text into a bytes object that can be used for the ``file`` or ``files`` parameters
    of :meth:`discord.abc.Messageable.send`.
    """
    file = BytesIO(text.encode(encoding))
    return discord.File(file, filename, spoiler=spoiler)
