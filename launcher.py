import sys
import logging
import asyncio
import discord
import importlib
import contextlib
import asyncpg

import config
import traceback

from bot import Obsidion

# nice and fast async system
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


@contextlib.contextmanager
def setup_logging():
    try:
        # __enter__
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        fmt = logging.Formatter(
            "[{asctime}] [{levelname:<7}] {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


async def create_pool(creds):
    pool = await asyncpg.create_pool(creds)
    return pool


def run_bot():
    log = logging.getLogger()
    loop = asyncio.get_event_loop()

    try:
        pool = loop.run_until_complete(create_pool(config.postgresql))
    except Exception as e:
        print("Could not load Postgres database", file=sys.stderr)
        log.exception("Could not load database Exiting.")
        return

    bot = Obsidion()
    bot.pool = pool
    bot.run()


def main():
    """Launches the bot."""
    loop = asyncio.get_event_loop()
    with setup_logging():
        run_bot()


if __name__ == "__main__":
    main()
