import time
import logging
import os

import discord
from discord.ext import tasks

import config
from services import userdata

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)

# Create a logger
logger = logging.getLogger("discord.jamtime")
logger.info("Logging initialized.")

# Init bot
bot = discord.Bot()
logger.info("Bot initialized")

# Check if development mode is enabled
if config.IS_DEV:
    logger.warning("Development mode is enabled. This may affect bot behavior.")
else:
    logger.info("Running in production mode.")

# Ensure the database file exists
userdata.initialize_db(config.DB_PATH)

# Dynamically load cogs
if os.path.exists(config.COGS_DIRECTORY):
    for filename in os.listdir(config.COGS_DIRECTORY):
        if filename.endswith(".py"):
            cog_name = filename[:-3]  # Remove the .py extension
            try:
                bot.load_extension(f"cogs.{cog_name}")
                logger.info(f"Loaded cog: {cog_name}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog_name}: {e}")


# Reminder task
@tasks.loop(seconds=30)
async def reminder():
    logger.info("Running reminder task...")
    t1 = time.time()
    data = userdata.get_db_data(config.DB_PATH)
    logger.debug(f"Loaded {len(data)} entries from the database.")

    if not data:
        logger.info("Skipping reminder task (empty database).")
        return

    updated = False
    for key, entry in data.items():
        if not entry.get("active"):
            logger.debug(f"Skipping inactive entry: {key}")
            continue

        logger.debug(f"Processing key: {key}")
        now = time.time()
        elapsed = now - entry.get("start_time", now)
        total = entry.get("end_time", now) - entry.get("start_time", now)

        message = None

        name = entry.get("name", key)
        short_id = entry.get("short_id", key)
        # End timer
        if elapsed > total:
            message = f"Timer {name}(`{short_id}`) has ended."
            entry["active"] = False
            updated = True

        # Halfway mark
        elif elapsed > total / 2 and not entry.get("halfway", False):
            message = (
                f"Timer {name}(`{short_id}`) is half way done. "
                f"It ends <t:{round(entry.get('end_time', now))}:R>."
            )
            entry["halfway"] = True
            updated = True

        if message:
            for user_id in entry.get("subscribers", []):
                try:
                    user = await bot.fetch_user(user_id)
                    channel = await user.create_dm()
                    await channel.send(message)
                except Exception as e:
                    logger.error(f"Failed to send reminder to {user_id}: {e}")

    if updated:
        userdata.write_db_data(config.DB_PATH, data)
    t2 = time.time()
    logger.info(
        f"Reminder task completed in {round(t2 - t1, 3)} seconds. Processed {len(data)} entries."
    )


# Cleanup task
#! this is unused for now because i dont want to mess something up
@tasks.loop(hours=1)
async def cleanup():
    logging.info("Running cleanup task...")
    t1 = time.time()
    data = userdata.get_db_data(config.DB_PATH)
    logging.debug(f"Loaded {len(data)} entries from the database.")

    deleted = 0

    if len(data) == 0:
        logger.warning("Empty database (cleanup)")
        return

    for key in list(data.keys()):
        entry = data[key]
        if entry["active"] is True:
            continue

        logging.debug(f"Removing inactive entry: {key}")
        del data[key]
        deleted += 1

    userdata.write_db_data(config.DB_PATH, data)
    t2 = time.time()
    logger.info(
        f"Cleanup task completed in {round(t2 - t1, 3)} seconds. Processed {len(data)} entries. Deleted {deleted} inactive entries."
    )


# Startup
@bot.event
async def on_ready():
    logger.info(f"Bot is logged in as {bot.user.name}#{bot.user.discriminator}")

    # cleaning up is for losers
    # cleanup.start()
    # logger.info("Started cleanup task")

    reminder.start()
    logger.info("Started reminder task")


# Running
bot.run(config.DISCORD_TOKEN)  # 🩹 i pray this holds together
