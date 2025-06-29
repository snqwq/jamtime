import config

import discord
from discord.ext import commands


# Init bot
bot = discord.Bot()


# Startup
@bot.event
async def on_ready():
    print(f"bot is logged in as {bot.user.name}#{bot.user.discriminator}")


# Running
bot.run(config.DISCORD_TOKEN)
