import config
import time

import discord
from discord.ext import commands


# Init bot
bot = discord.Bot()


# Commands
@bot.slash_command(
    name="hello",
    description="Says hello world not much more to it",
    guild_ids=config.get_guild_ids(),
)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(f"Hello {ctx.author}!")


@bot.slash_command(
    name="timetest",
    description="bluh",
    guild_ids=config.get_guild_ids(),
)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(f"current time is {time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time()))}, idiot")



# Startup
@bot.event
async def on_ready():
    print(f"bot is logged in as {bot.user.name}#{bot.user.discriminator}")


# Running
bot.run(config.DISCORD_TOKEN)
