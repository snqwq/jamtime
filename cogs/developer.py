import time

import discord
from discord.ext import commands
from config import get_guild_ids


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="hello",
        description="Says hello world not much more to it",
        guild_ids=get_guild_ids(),
    )
    async def hello(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Hello {ctx.author.id}!")

    @discord.slash_command(
        name="timetest",
        description="Checks what the current time is",
        guild_ids=get_guild_ids(),
    )
    async def hello(self, ctx: discord.ApplicationContext):
        await ctx.respond(
            f"current time is {time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time()))}"
        )


def setup(bot):
    bot.add_cog(Developer(bot))
