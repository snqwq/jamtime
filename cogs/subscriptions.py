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

        user_subscriptions = userdata.get_user_subscriptions(DB_PATH, user_id)

        await ctx.respond(
            f"You are subscribed to: {user_subscriptions}",
        )

    @discord.slash_command(
        name="unsubscribe",
        description="bluh",
        guild_ids=get_guild_ids(),
    )
    @discord.option("timer_id", description="id of timer to unsubscribe from")
    async def unsubscribe(self, ctx: discord.ApplicationContext, timer_id: str):
        user_id = ctx.author.id

        data = userdata.get_db_data(DB_PATH)
        for key, value in data.items():
            if key == timer_id:
                value["subscribers"].remove(user_id)
                userdata.write_db_data(DB_PATH, data)
                break

        await ctx.respond(f"unsubscribed from {timer_id}")

    @discord.slash_command(
        name="subscribe",
        description="bluh",
        guild_ids=get_guild_ids(),
    )
    @discord.option("timer_id", description="id of timer to subscribe to")
    async def unsubscribe(ctx: discord.ApplicationContext, timer_id: str):
        user_id = ctx.author.id

        data = userdata.get_db_data(DB_PATH)
        for key, value in data.items():
            if key == timer_id:
                value["subscribers"].append(user_id)
                userdata.write_db_data(DB_PATH, data)
                break

        await ctx.respond(f"subscribed to {timer_id}")


def setup(bot):
    bot.add_cog(Subscriptions(bot))
