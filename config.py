from dotenv import load_dotenv
import os

# Variables
VERSION = "1.0.0"
DEV_GUILD_IDS = [1389020690505531422]
DEV_USER_IDS = [686709101044039769]
DB_PATH = "database.json"
COGS_DIRECTORY = "cogs"

# Load environment variables from .env file
try:
    load_dotenv()
except Exception as e:
    print(f"Error loading .env file: {e}")

# Load environment variables into python variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in the environment variables.")

if os.getenv("IS_DEV") is not None:
    IS_DEV = os.getenv("IS_DEV").lower() in ("true", "1", "yes")
else:
    IS_DEV = False


# Helper functions
def get_guild_ids():
    return DEV_GUILD_IDS if IS_DEV else None
