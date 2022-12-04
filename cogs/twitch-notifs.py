import re

from discord.ext import commands
import json


class Dev(commands.Cog):
    """Development stuff"""

    def __init__(self, bot):
        self.bot = bot
        self.load_json_storage()

    def load_json_storage(self):
        with open("./data.json") as f:
            self.data = json.loads(f.read())
            self.data = self.data["notifications"]

    async def save_data(self):
        with open("./data.json", "w") as f:
            self.new_data = {}
            self.new_data["notifications"] = list(set(self.data))
            print(self.new_data)
            f.write(json.dumps(self.new_data))

    @commands.group(name="notifications")
    async def notifications(self, ctx):
        """Manage all stream notifications here"""
        if ctx.invoked_subcommand is None:
            await (ctx.send('Invaid sub-command passed'))

    @notifications.command()
    async def add(self, ctx, streamer_username: str):
        """Adds a streamer to the automatic notifications."""
        try:
            self.data.append(streamer_username)
            await self.save_data()
            await ctx.send(f"Successfully added {streamer_username} to the watchlist, and saved the data file")
        except Exception as e:
            await ctx.send(f"Failed to add {streamer_username} to the watchlist because of \n{e}")

    @notifications.command()
    async def remove(self, ctx, streamer_username: str):
        """Removes a streamer to the automatic notifications."""
        try:
            self.data.pop(self.data.index(streamer_username))
            await self.save_data()
            await ctx.send(f"Successfully removed {streamer_username} from the watchlist, and saved the data file")
        except Exception as e:
            await ctx.send(f"Failed to remove {streamer_username} from the watchlist because of \n{e}")

    @notifications.command()
    async def list(self, ctx):
        """Lists all the channels currently in the watchlist"""
        await ctx.send(f"The current watchlist is: {self.data}")


def setup(bot):
    bot.add_cog(Dev(bot))
