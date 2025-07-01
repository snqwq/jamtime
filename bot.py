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

    new_start_time = time.time()
    new_end_time = new_start_time + 60*duration

    await ctx.respond(
       f"started {name}: {unique_id}, ends at {time.strftime('%Y-%m-%d %H:%M %Z',  time.localtime(new_end_time))}"
    )

    data = get_db_data()

    # Updates data with new user
    data[f"{uuid.uuid4()}"] = {
        "start_time": new_start_time,
        "end_time": new_end_time,
        "subscribers": [ctx.author.id]
    }
    print(data)

    write_db_data(data)

# x = {
#     "database": {
       
#         "a6066e7a-d5dc-4707-8962-01a572112ce0": {
#             "start_time": 170000000,
#             "end_time": 1750000000,
#             "subscribers": ["bob", "aa"]
#         }
#     }
# }




@tasks.loop(seconds=5)
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
            message = f"TIMER DONEEEEEEEEEEEEE🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘 {elapsed_time}/{total_time}"
            # Terminate db entry

            new_data = get_db_data()
            del new_data[key]
            write_db_data(new_data)

            
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
