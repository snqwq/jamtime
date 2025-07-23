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
                active_timers.append(
                    f"{value["name"]} ({value['short_id']}) - <t:{round(value['end_time'])}:R>"
                )

        if not active_timers:
            description = "No active timers."
        else:
            description = "\n".join(active_timers)
        if len(description) > 2048:
            description = "Too many active timers to display."
        embed = discord.Embed(
            title="Active Timers",
            description=description,
            color=discord.Color.red(),
        )
        await ctx.respond(embed=embed)

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
    @discord.option("duration", description="desired timer duration", input_type=int)
    @discord.option(
        "unit",
        description="unit of time (seconds, minutes, hours, days)",
        input_type=str,
    )
    async def start(
        self, ctx: discord.ApplicationContext, name: str, duration: int, unit: str
    ):
        unique_id = str(uuid.uuid4())

        duration_in_seconds = 0
        if unit == "seconds":
            duration_in_seconds = int(duration)
        elif unit == "minutes":
            duration_in_seconds = int(duration) * 60
        elif unit == "hours":
            duration_in_seconds = int(duration) * 3600
        elif unit == "days":
            duration_in_seconds = int(duration) * 86400
        else:
            await ctx.respond(
                "Invalid unit of time. Please use seconds, minutes, hours, or days."
            )
            return

        start_time = time.time()
        end_time = start_time + duration_in_seconds
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
            "creator": ctx.author.id,
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
    @discord.option("id", description="ID of the timer to stop")
    async def stop(self, ctx: discord.ApplicationContext, id: str):
        key = userdata.short_id_to_key(DB_PATH, id)
        data = userdata.get_db_data(DB_PATH)

        timer = data.get(key)

        if not timer:
            await ctx.respond(f"Timer with ID `{id}` not found. (is it active?)")
            return

        if not timer["active"]:
            await ctx.respond(f"Timer **{timer['name']}** is already stopped.")
            return

        if timer["creator"] != ctx.author.id:
            await ctx.respond("You can only stop timers that you have created.")
            return

        timer["active"] = False
        userdata.write_db_data(DB_PATH, data)

        await ctx.respond(f"Timer **{timer['name']}** has been stopped.")


def setup(bot):
    bot.add_cog(Timers(bot))
