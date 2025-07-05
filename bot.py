import time
import json
import logging
import os

import discord
from discord.ext import commands, tasks
from discord import option

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
    logging.info("Running reminder task...")
    t1 = time.time()
    data = userdata.get_db_data(config.DB_PATH)
    logging.debug(f"Loaded {len(data)} entries from the database.")

    if len(data) == 0:
        logger.warning("Empty database (reminders)")
        return

    for key in data:
        entry = data[key]
        if entry["active"] is False:
            logging.debug(f"Skipping inactive entry: {key}")
            continue

        logging.debug(f"Processing key: {key}")
        elapsed_time = time.time() - entry["start_time"]
        total_time = entry["end_time"] - entry["start_time"]

        message = None

        # End timer
        if elapsed_time > total_time:
            message = f"Timer {entry['name']} has ended."
            # Terminate db entry

            entry["active"] = False

        # Half way mark
        elif elapsed_time > total_time / 2:
            if entry["halfway"] == False:
                # Notify subscribers
                message = f"Timer {entry['name']} is half way done. It will end <t:{round(entry['end_time'])}:R>."
                entry["halfway"] = True

        if message:
            subscribers = entry["subscribers"]
            for user_id in subscribers:
                user = await bot.fetch_user(user_id)
                channel = await bot.create_dm(user)
                await channel.send(message)

    userdata.write_db_data(config.DB_PATH, data)
    t2 = time.time()
    logger.info(
        f"Reminder task completed in {round(t2 - t1, 3)} seconds. Processed {len(data)} entries."
    )


# Cleanup task
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

    # cleanup.start()
    # logger.info("Started cleanup task")

    reminder.start()
    logger.info("Started reminder task")


# Running
bot.run(config.DISCORD_TOKEN)
