import json

data = []
with open("cogs/servers/data.json") as f:
    data.append(json.load(f))

data = data[0]['player']
print(data['achievements'])