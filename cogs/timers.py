import dis
import uuid
import time
import random
import string

import discord
from discord.ext import commands
from config import get_guild_ids, DB_PATH

from services import userdata


class Timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    timer_group = discord.SlashCommandGroup("timer")

    @timer_group.command(
        name="active",
        description="Lists all active timers",
        guild_ids=get_guild_ids(),
    )
    async def active_timers(self, ctx: discord.ApplicationContext):

        active_timers = []

        data = userdata.get_db_data(DB_PATH)
        for key, value in data.items():
            if value["active"]:
                active_timers.append(f"{value["name"]} ({key})")

        await ctx.respond(f"active timers: {active_timers}")

    @timer_group.command(
        name="properties",
        description="Get properties of a timer",
        guild_ids=get_guild_ids(),
    )
    @discord.option("id", description="id of timer to subscribe to")
    async def timer_properties(self, ctx: discord.ApplicationContext, id: str):

        properties = None

        data = userdata.get_db_data(DB_PATH)
        for key, value in data.items():
            if key == id:
                properties = value
                break

        await ctx.respond(f"timer properties: {properties}")

    @timer_group.command(
        name="new",
        description="make a new timer",
        guild_ids=get_guild_ids(),
    )
    @discord.option("name", description="desired name", input_type=str)
    @discord.option(
        "duration", description="desired timer duration in minutes", input_type=int
    )
    async def start(
        self, ctx: discord.ApplicationContext, duration: int, name: str, start: bool
    ):
        unique_id = str(uuid.uuid4())

        start_time = time.time()
        end_time = start_time + 60 * duration
        short_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

        data = userdata.get_db_data(DB_PATH)

        # Updates data with new user
        data[f"{unique_id}"] = {
            "name": name,
            "short_id": short_id,
            "active": True,
            "halfway": False,
            "start_time": start_time,
            "end_time": end_time,
            "subscribers": [ctx.author.id],
        }

        userdata.write_db_data(DB_PATH, data)

        embed = discord.Embed(
            title="Timer Started",
            description=f"Timer **{name}** has been started with a duration of **{duration} minute(s)**.",
            color=discord.Color.red(),
        )

        embed.add_field(name="ID", value=f"`{short_id}`", inline=False)
        embed.add_field(
            name="Started", value=f"<t:{round(start_time)}:F>", inline=False
        )
        embed.add_field(
            name="Ends",
            value=f"<t:{round(end_time)}:F> (<t:{round(end_time)}:R>)",
            inline=False,
        )

        embed.set_footer(text=unique_id)

        await ctx.respond(embed=embed)

    @timer_group.command(
        name="stop",
        description="stop a timer",
        guild_ids=get_guild_ids(),
    )
    @discord.option("id", description="ID (short) of the timer to stop")
    async def stop_timer(self, ctx: discord.ApplicationContext, id: str):
        key = userdata.short_id_to_key(DB_PATH, id)
        data = userdata.get_db_data(DB_PATH)

        timer = data.get(key)

        if not timer:
            await ctx.respond(f"Timer with ID `{id}` not found. (is it active?)")
            return

        timer["active"] = False
        userdata.write_db_data(DB_PATH, data)

        await ctx.respond(f"Timer **{timer['name']}** has been stopped.")


def setup(bot):
    bot.add_cog(Timers(bot))
