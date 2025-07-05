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


# Task
@tasks.loop(seconds=60)
async def reminder():
    data = userdata.get_db_data(config.DB_PATH)

    if len(data) == 0:
        logger.warning("Empty database (reminders)")
        return

    for key in data:
        entry = data[key]

        elapsed_time = time.time() - entry["start_time"]
        total_time = entry["end_time"] - entry["start_time"]

        message = None

        # End timer
        if elapsed_time > total_time:
            message = f"TIMER DONEEEEEEEEEEEEE🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘 {elapsed_time}/{total_time}"
            # Terminate db entry

            del data[key]
            userdata.write_db_data(config.DB_PATH, data)

        # Half way mark
        elif elapsed_time > total_time / 2:
            # Notify subscribers
            message = f"{elapsed_time}/{total_time}"

        if not message:
            return

        subscribers = entry["subscribers"]
        for user_id in subscribers:

            user = await bot.fetch_user(user_id)
            channel = await bot.create_dm(user)
            await channel.send(message)


# Startup
@bot.event
async def on_ready():
    logger.info(f"Bot is logged in as {bot.user.name}#{bot.user.discriminator}")

    reminder.start()
    logger.info("Started reminder task")


# Running
bot.run(config.DISCORD_TOKEN)
