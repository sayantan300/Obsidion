
# at some point I will move to Postgres but
# today is not that day

import json
from collections import OrderedDict

class Data():
    def __init__(self):
        pass

    def connect(self):
        """ Load the json file"""
        with open("data.json") as f:
            data = json.load(f)
        return data

    def save(self, data):
        """Save the json file"""
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
        return