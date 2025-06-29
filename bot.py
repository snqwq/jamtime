import config

import discord
from discord.ext import commands


# Init bot
bot = discord.Bot()


# Commands
@bot.slash_command(
    name="Hello",
    description="Says hello world not much more to it",
    guild_ids=config.get_guild_ids(),
)
async def hello(self, ctx: discord.ApplicationContext):
    
        @discord.slash_command(
        name="hello", description="Make the bot say hello", guild_ids=get_guild_ids()
    )
    async def hello(self, ctx: discord.ApplicationContext):
        """Make the bot say hello to the user (helps check some permissions)"""
        await ctx.respond(f"Hello {ctx.author}!")
    

# Startup
@bot.event
async def on_ready():
    print(f"bot is logged in as {bot.user.name}#{bot.user.discriminator}")


# Running
bot.run(config.DISCORD_TOKEN)
