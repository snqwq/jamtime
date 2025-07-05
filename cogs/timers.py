import uuid
import time

import discord
from discord.ext import commands
from config import get_guild_ids, DB_PATH

from services import userdata


class Timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="active_timers",
        description="bluh",
        guild_ids=get_guild_ids(),
    )
    async def active_timers(self, ctx: discord.ApplicationContext):

        active_timers = []

        data = userdata.get_db_data(DB_PATH)
        for key, value in data.items():
            active_timers.append(f"{value["name"]} ({key})")

        await ctx.respond(f"active timers: {active_timers}")

    @discord.slash_command(
        name="timer_properties",
        description="bluh",
        guild_ids=get_guild_ids(),
    )
    @discord.option("timer_id", description="id of timer to subscribe to")
    async def timer_properties(self, ctx: discord.ApplicationContext, timer_id: str):

        properties = None

        data = userdata.get_db_data(DB_PATH)
        for key, value in data.items():
            if key == timer_id:
                properties = value
                break

        await ctx.respond(f"timer properties: {properties}")

    @discord.slash_command(
        name="start",
        description="bluh",
        guild_ids=get_guild_ids(),
    )
    @discord.option("name", description="desired name")
    @discord.option("duration", description="desired timer duration")
    async def start(self, ctx: discord.ApplicationContext, duration: int, name: str):
        unique_id = str(uuid.uuid4())

        start_time = time.time()
        end_time = start_time + 60 * duration

        await ctx.respond(
            f"started {name}: {unique_id}, ends on <t:{round(end_time)}:F>"
        )

        data = userdata.get_db_data(DB_PATH)

        # Updates data with new user
        data[f"{uuid.uuid4()}"] = {
            "start_time": start_time,
            "end_time": end_time,
            "subscribers": [ctx.author.id],
            "name": name,
        }

        userdata.write_db_data(DB_PATH, data)


def setup(bot):
    bot.add_cog(Timers(bot))
