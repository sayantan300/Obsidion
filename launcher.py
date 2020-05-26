import sys
import logging
import asyncio
import contextlib
import asyncpg

import config

from bot import Obsidion

# nice and fast async system
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def run_bot():
    loop = asyncio.get_event_loop()

    try:
        pool = loop.run_until_complete(connect_pool(config.postgresql))
    except Exception:
        print("Could not load Postgres database", file=sys.stderr)
        return

    bot = Obsidion()
    bot.pool = pool
    bot.run()


def main():
    """Launches the bot."""
    run_bot()


async def connect_pool(password):
    """connect to the pool"""
    pool = await asyncpg.create_pool(f"postgresql://discord:{password}@db/discord")
    return pool


if __name__ == "__main__":
    main()
