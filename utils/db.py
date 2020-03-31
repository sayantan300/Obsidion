# These are just things that allow me to make tables for PostgreSQL easier
# This isn't exactly good. It's just good enough for my uses.
# Also shoddy migration support.

from pathlib import Path
import json
import os
import pydoc
import uuid
import datetime
import inspect
import decimal
#import asyncpg
import logging
import asyncio
import json


log = logging.getLogger(__name__)

class Data():
    def __init__(self):
        pass

    def connect(self):
        with open("data.json") as f:
            data = json.load(f)
        return data

    def save(self, data):
        with open("data.json", "r+") as f:
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate

    