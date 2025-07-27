import discord
from discord.ext import commands
from config import get_guild_ids, DB_PATH

from services import userdata


class Subscriptions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="subscriptions",
        description="Lists your subscriptions",
        guild_ids=get_guild_ids(),
    )
    async def subscriptions(self, ctx: discord.ApplicationContext):
        user_id = ctx.author.id
        data = userdata.get_db_data(DB_PATH)
        user_subscriptions = userdata.get_user_subscriptions(DB_PATH, user_id)

        description = ""

        if user_subscriptions:
            for key in user_subscriptions:
                entry = data[key]
                description += f"\n**{entry['name']}** (`{entry['short_id']}`) - " f"<t:{round(entry['end_time'])}:R>"
        else:
            description = "You are not subscribed to any timers."

        embed = discord.Embed(
            title="Your Subscriptions",
            description=description,
            color=discord.Color.red(),
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(
        name="unsubscribe",
        description="Unsubscribe from a timer",
        guild_ids=get_guild_ids(),
    )
    @discord.option("id", description="ID of the timer to unsubscribe from")
    async def unsubscribe(self, ctx: discord.ApplicationContext, id: str):
        user_id = ctx.author.id

        data = userdata.get_db_data(DB_PATH)
        key = userdata.short_id_to_key(DB_PATH, id)

        if not key:
            await ctx.respond(f"Timer with id {id} not found.")
            return

        for subscriber in data[key]["subscribers"]:
            if subscriber == user_id:
                data[key]["subscribers"].remove(user_id)
                userdata.write_db_data(DB_PATH, data)
                break

        name = data[key]["name"]

        await ctx.respond(f"Unsubscribed from timer {name} (`{id}`)")

    @discord.slash_command(
        name="subscribe",
        description="Subscribe to a timer",
        guild_ids=get_guild_ids(),
    )
    @discord.option("id", description="ID of timer to subscribe to")
    async def subscribe(ctx: discord.ApplicationContext, id: str):
        user_id = ctx.author.id

        data = userdata.get_db_data(DB_PATH)
        key = userdata.short_id_to_key(DB_PATH, id)

        if not key:
            await ctx.respond(f"Timer with id {id} not found.")
            return

        for subscriber in data[key]["subscribers"]:
            if subscriber == user_id:
                await ctx.respond(f"You are already subscribed to {id}.")
                return

        data[key]["subscribers"].append(user_id)
        userdata.write_db_data(DB_PATH, data)

        name = data[key]["name"]

        await ctx.respond(f"Subscribed to timer {name} (`{id}`)")


def setup(bot):
    bot.add_cog(Subscriptions(bot))


if __name__ == "__main__":
    print("This cog is not meant to be run directly. Please load it with the bot.")
