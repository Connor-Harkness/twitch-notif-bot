import re
import twitch
import config
from datetime import datetime, timedelta
import discord
import time
from discord.ext import commands, tasks
import json


class Dev(commands.Cog):
    """Development stuff"""

    def __init__(self, bot):
        self.bot = bot
        self.load_json_storage()
        self.helix = twitch.Helix(config.client_id, config.client_secret, use_cache=True,
                                  cache_duration=timedelta(minutes=10))
        time.sleep(10)
        self.check_if_live.start()
        self.posted = {}
        for streamer in self.data:
            self.posted[streamer] = None

    def cog_unload(self):
        self.check_if_live.cancel()

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

    @commands.command()
    async def test(self, ctx, strmr):
        await ctx.send(strmr.data)
        # await ctx.send(f"searched for: {strmr}\n got: {self.helix.user(strmr).data}")

    @tasks.loop(seconds=60)
    async def check_if_live(self):

        for streamer in self.data:

            user = self.helix.user(streamer).data
            try:
                stream = self.helix.stream(user_id=user["id"]).data

                if stream["type"] == "live":

                    if self.posted[streamer] == None:
                        emb = await self.sendemb(user, stream)
                        self.posted[streamer] = emb.id
                else:
                    self.posted[streamer] = None

            except Exception as e:
                print(f"{e}")

    async def sendemb(self, user, stream):
        # {
        #     "type": "rich",
        #     "title": `streamer is live!`,
        #     "description": `stream description`,
        #     "color": 0x00FFFF,
        #     "image": {
        #         "url": `stream preview`,
        #     "thumbnail": {
        #         "url": `streamer profile pic`,
        #     },
        #     "url": `stream url`

        e = discord.Embed()
        e.url = f"https://twitch.tv/{user['login']} "
        e.title = f"{user['display_name']} is LIVE :red_circle: NOW!"
        e.description = f"**{stream['title']}**\n{user['description']}"
        e.color = 0x00FFFF
        new_url = stream["thumbnail_url"]
        width = 1024
        height = 768
        e.set_image(url=new_url.format(width=1024,
                                       height=768))
        e.set_thumbnail(url=user["profile_image_url"])

        c = await self.bot.fetch_channel(config.notification_channel)
        emb = await c.send(embed=e)
        return emb


def setup(bot):
    bot.add_cog(Dev(bot))
