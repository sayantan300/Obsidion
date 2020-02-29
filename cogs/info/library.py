import requests

def status():
    """Check the status of the mojang services"""

    response = requests.get(f"https://api.mojang.com/")
    data = response.json()

    return data

def get_uuid(username):
    """Get the uuid of a username and return false if it is not being used"""

    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if response.status_code == 200:
        data = response.json()
        uuid = data["id"]
        return uuid
    else:
        return False

def names(uuid):
    """Get all the names of a minecraft player"""

    response = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names")
    data = response.json()

    return data



