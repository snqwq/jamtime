import time
import json
import uuid
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


# Commands


@bot.slash_command(
    name="subscriptions",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
async def subscriptions(ctx: discord.ApplicationContext):

    user_id = ctx.author.id
    user_subscriptions = userdata.get_user_subscriptions(config.DB_PATH, user_id)

    await ctx.respond(f"subscribed to: {user_subscriptions}")


@bot.slash_command(
    name="unsubscribe",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
@option("timer_id", description="id of timer to unsubscribe from")
async def unsubscribe(ctx: discord.ApplicationContext, timer_id: str):
    user_id = ctx.author.id

    data = userdata.get_db_data(config.DB_PATH)
    for key, value in data.items():
        print(data)
        if key == timer_id:
            value["subscribers"].remove(user_id)
            userdata.write_db_data(config.DB_PATH, data)
            break

    await ctx.respond(f"unsubscribed from {timer_id}")


@bot.slash_command(
    name="subscribe",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
@option("timer_id", description="id of timer to subscribe to")
async def unsubscribe(ctx: discord.ApplicationContext, timer_id: str):
    user_id = ctx.author.id

    data = userdata.get_db_data(config.DB_PATH)
    for key, value in data.items():
        print(data)
        if key == timer_id:
            value["subscribers"].append(user_id)
            userdata.write_db_data(config.DB_PATH, data)
            break

    await ctx.respond(f"subscribed to {timer_id}")


@bot.slash_command(
    name="active_timers",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
async def active_timers(ctx: discord.ApplicationContext):

    active_timers = []

    data = userdata.get_db_data(config.DB_PATH)
    for key, value in data.items():
        active_timers.append(f"{value["name"]} ({key})")

    await ctx.respond(f"active timers: {active_timers}")


@bot.slash_command(
    name="timer_properties",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
@option("timer_id", description="id of timer to subscribe to")
async def timer_properties(ctx: discord.ApplicationContext, timer_id: str):

    properties = None

    data = userdata.get_db_data(config.DB_PATH)
    for key, value in data.items():
        if key == timer_id:
            properties = value
            break

    await ctx.respond(f"timer properties: {properties}")


@bot.slash_command(
    name="start",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
@option("name", description="desired name")
@option("duration", description="desired timer duration")
async def start(ctx: discord.ApplicationContext, duration: int, name: str):
    unique_id = str(uuid.uuid4())

    start_time = time.time()
    end_time = start_time + 60 * duration

    await ctx.respond(
        f"started {name}: {unique_id}, ends at {time.strftime('%Y-%m-%d %H:%M %Z',  time.localtime(end_time))}"
    )

    data = userdata.get_db_data(config.DB_PATH)

    # Updates data with new user
    data[f"{uuid.uuid4()}"] = {
        "start_time": start_time,
        "end_time": end_time,
        "subscribers": [ctx.author.id],
        "name": name,
    }
    print(data)

    userdata.write_db_data(config.DB_PATH, data)


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
