from typing import Optional, SupportsInt


async def get(session, url: str, params=None, json=None):
    """get the json from a webpage"""
    async with session.get(url, params=params, json=json) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data
        return False


async def get_uuid(session, username):
    """get the uuid using username"""
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.json()
            uuid = data["id"]
            return uuid
        return False
