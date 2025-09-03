import os
from dotenv import load_dotenv
from utils import DynamicConfig

load_dotenv(override=True)

def get_config():
    return DynamicConfig(
        {
            "name": os.getenv("NAME", "Void"),
            "session": os.getenv("SESSION", "db.sqlite3"),
            "number": os.getenv("NUMBER"),
            "prefix": os.getenv("PREFIX", "#"),
            "uri": os.getenv("URI"),
            "mods": (
                os.getenv("MODS", "").split(",") if os.getenv("MODS") else []
            ),
            "dev": (
                os.getenv("DEV", "").split(",") if os.getenv("DEV") else []
            ),
        }
    )
