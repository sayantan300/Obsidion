

async def get(session, url):
    """get the json from a webpage"""
    async with session.get(url) as resp:
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

async def uuid_from_username(username, session, bot, ctx):
    """get the uuid or check in db"""
    if username:
        uuid = await get_uuid(session, username)
    elif await bot.pool.fetchval(
        "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
    ):
        uuid = await bot.pool.fetchval(
            "SELECT uuid FROM discord_user WHERE id = $1", ctx.author.id
        )
        names = await get(
            session, f"https://api.mojang.com/user/profiles/{uuid}/names"
        )
        username = names[-1]["name"]
    else:
        uuid = False
    
    return uuid, username


def load_from_text(file):
    """load a file from a text file"""
    with open(f"cogs/fun/{file}.txt") as f:
        content = f.readlines()
    return [x.strip() for x in content]
