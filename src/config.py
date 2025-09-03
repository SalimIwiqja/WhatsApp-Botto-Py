import os
from dotenv import load_dotenv
from utils import DynamicConfig

# Load .env file (always override so new values apply)
load_dotenv(override=True)

def get_config():
    return DynamicConfig(
        {
            "name": os.getenv("NAME", "Void"),  # bot name
            "session": os.getenv("SESSION", "db.sqlite3"),  # session file
            "number": os.getenv("NUMBER"),  # bot's own number (JID style later)
            "prefix": os.getenv("PREFIX", "#"),  # bot prefix (# by default)
            "uri": os.getenv("URI"),  # DB or API uri if needed

            # Moderators list (comma-separated numbers in .env)
            "mods": os.getenv("MODS", "").replace(" ", "").split(",") if os.getenv("MODS") else [],

            # Developers list (comma-separated numbers in .env)
            "dev": os.getenv("DEV", "").replace(" ", "").split(",") if os.getenv("DEV") else [],
        }
    )
