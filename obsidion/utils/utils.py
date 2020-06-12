from typing import Optional, SupportsInt


async def get(session, url: str, params=None, json=None):
    """get the json from a webpage"""
    async with session.get(url, params=params, json=json) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data
        return False
