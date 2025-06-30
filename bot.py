import config
import time
import json
import uuid

import discord
from discord.ext import commands, tasks
from discord import option


# Init bot
bot = discord.Bot()


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

    await ctx.respond(
       f"started {name}: {unique_id}, ends at {time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time() + 3600*duration))}"
    )


    # Write new session to db

    #file_path = "database.json"
    with open("database.json", "a") as f:
        json.dump(
            f"{unique_id}",
            f,
            indent=4
        )
        

# # Append to database
# file_path = "database.json"
# with open(file_path, "a") as f:
#   json.dump(x, f, indent=4)

# with open(file_path) as f:
#   print(f.read())


# x = {
#     "database": {
       
#         "a6066e7a-d5dc-4707-8962-01a572112ce0": {
#             "start_time": 170000000,
#             "end_time": 1750000000,
#             "subscribers": ["bob", "aa"]
#         }
#     }
# }




@tasks.loop(minutes=10)
async def reminder(self):
    pass


# Startup
@bot.event
async def on_ready():
    print(f"bot is logged in as {bot.user.name}#{bot.user.discriminator}")


# Running
bot.run(config.DISCORD_TOKEN)
