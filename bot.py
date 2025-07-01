import config
import time
import json
import uuid

import discord
from discord.ext import commands, tasks
from discord import option


# Init bot
bot = discord.Bot()

DB_PATH = "database.json"

def get_db_data():
    with open(DB_PATH, "r") as f:
        data = json.load(f)
    return data

def write_db_data(new_data):
    with open(DB_PATH, "w") as f:
        json.dump(new_data, f, indent=4)



# Commands
@bot.slash_command(
    name="hello",
    description="Says hello world not much more to it",
    guild_ids=config.get_guild_ids(),
)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(f"Hello {ctx.author.id}!")



@bot.slash_command(
    name="timetest",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(f"current time is {time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time()))}, idiot")



@bot.slash_command(
    name="subscriptions",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
async def subscriptions(ctx: discord.ApplicationContext):

    user_id = ctx.author.id
    user_subscriptions = []
    
    data = get_db_data()
    for key in data:
        entry = data[key]
        for subscriber in entry["subscribers"]:
            if subscriber == user_id:
                user_subscriptions.append(f"{entry["name"]} ({key})")
                break

    await ctx.respond(f"subscribed to: {user_subscriptions}")


@bot.slash_command(
    name="unsubscribe",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
@option("timer_id", description="id of timer to unsubscribe from")
async def unsubscribe(
    ctx: discord.ApplicationContext,
    timer_id: str
):
    user_id = ctx.author.id
    
    data = get_db_data()
    for key, value in data.items():
        print(data)
        if key == timer_id:
            value["subscribers"].remove(user_id)
            write_db_data(data)
            break

    await ctx.respond(f"unsubscribed from {timer_id}")



@bot.slash_command(
    name="subscribe",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
@option("timer_id", description="id of timer to subscribe to")
async def unsubscribe(
    ctx: discord.ApplicationContext,
    timer_id: str
):
    user_id = ctx.author.id
    
    data = get_db_data()
    for key, value in data.items():
        print(data)
        if key == timer_id:
            value["subscribers"].append(user_id)
            write_db_data(data)
            break

    await ctx.respond(f"subscribed to {timer_id}")


@bot.slash_command(
    name="active_timers",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
async def active_timers(ctx: discord.ApplicationContext):
    
    active_timers = []

    data = get_db_data()
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

    data = get_db_data()
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
async def start(
   ctx: discord.ApplicationContext,
   duration: int,
   name: str
):
    unique_id = str(uuid.uuid4())

    start_time = time.time()
    end_time = start_time + 60*duration

    await ctx.respond(
       f"started {name}: {unique_id}, ends at {time.strftime('%Y-%m-%d %H:%M %Z',  time.localtime(end_time))}"
    )

    data = get_db_data()

    # Updates data with new user
    data[f"{uuid.uuid4()}"] = {
        "start_time": start_time,
        "end_time": end_time,
        "subscribers": [ctx.author.id],
        "name": name,
    }
    print(data)

    write_db_data(data)




@tasks.loop(seconds=60)
async def reminder():
    data = get_db_data()
    
    if len(data) == 0:
        print("no data")
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
            write_db_data(data)

            
        # Half way mark
        elif elapsed_time > total_time / 2:
            # Notify subscribers
            message = f"{elapsed_time}/{total_time}"


        if not message: return

        subscribers = entry["subscribers"]
        for user_id in subscribers:

            user = await bot.fetch_user(user_id)
            channel = await bot.create_dm(user)
            await channel.send(message)



# Startup
@bot.event
async def on_ready():
    print(f"bot is logged in as {bot.user.name}#{bot.user.discriminator}")

    reminder.start()


# Running
bot.run(config.DISCORD_TOKEN)
