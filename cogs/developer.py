import time

import discord
from discord.ext import commands
from config import get_guild_ids, DEV_GUILD_IDS


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    dev_group = discord.SlashCommandGroup(name="dev", description="Developer commands")

    @dev_group.command(
        name="hello",
        description="Says hello world not much more to it",
        guild_ids=DEV_GUILD_IDS,
    )
    async def hello(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Hello {ctx.author.id}!")

    @dev_group.command(
        name="timetest",
        description="Checks what the current time is",
        guild_ids=DEV_GUILD_IDS,
    )
    async def timetest(self, ctx: discord.ApplicationContext):
        await ctx.respond(
            f"current time is {time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time()))}"
        )

    @dev_group.command(
        name="ping",
        description="Checks the bot's latency",
        guild_ids=DEV_GUILD_IDS,
    )
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)}ms")

    @dev_group.command(
        name="dm_echo",
        description="Echoes a message back to the user in a DM",
        guild_ids=DEV_GUILD_IDS,
    )
    async def dm_echo(self, ctx: discord.ApplicationContext, message: str):
        await ctx.author.send(message)
        await ctx.respond("Message sent!")


def setup(bot):
    bot.add_cog(Developer(bot))
