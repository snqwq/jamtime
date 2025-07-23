from dotenv import load_dotenv
import os

# Variables
VERSION = "0.0.1"
IS_DEV = True
DEV_GUILD_IDS = [1389020690505531422]
DEV_USER_IDS = [686709101044039769]
DB_PATH = "database.json"
COGS_DIRECTORY = "cogs"

# Load environment variables from .env file
load_dotenv()

# Load environment variables into python variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


# Helper functions
def get_guild_ids():
    return DEV_GUILD_IDS if IS_DEV else None
