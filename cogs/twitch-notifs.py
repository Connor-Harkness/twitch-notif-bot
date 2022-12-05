import json
import time
from datetime import timedelta

import config
import discord
import twitch
from discord.ext import commands, tasks


class TwitchNotifs(commands.Cog):
    """Twitch livestream notifications"""

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

    async def save_data(self):
        with open("./data.json", "w") as f:
            f.write(json.dumps(self.data))

    @commands.group(name="notifications")
    async def notifications(self, ctx):
        """Manage all stream notifications here"""
        if ctx.invoked_subcommand is None:
            await (ctx.send('Invaid sub-command passed'))

    @notifications.command()
    async def add(self, ctx, streamer_username: str, color: str = None):
        """Adds a streamer to the automatic notifications."""
        try:
            self.data[streamer_username] = {"color": color, "roles": None}
            await self.save_data()
            await ctx.send(f"Successfully added {streamer_username} to the watchlist, and saved the data file")
        except Exception as e:
            await ctx.send(f"Failed to add {streamer_username} to the watchlist because of \n{e}")

    @notifications.command()
    async def edit(self, ctx, streamer_username: str, key, value=None):
        """Edits the settings for a user in the watchlist
        USAGE: !notifications edit <streamer: connor_harkness> <key: colour> <value: 0x00FFFF>"""
        try:
            self.data[streamer_username][key] = value
            await self.save_data()
        except Exception as e:
            await ctx.send(f"Failed to edit: {streamer_username} \n {e}")

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

    @tasks.loop(seconds=60)
    async def check_if_live(self):
        for streamer in self.data:
            try:
                user = self.helix.user(streamer).data
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
        if self.data[user["login"]]["color"] != None:
            e.colour = int(self.data[user["login"]["color"]], 16)
        e.colour = 0x00FFFF
        new_url = stream["thumbnail_url"]
        e.set_image(url=new_url.format(width=1024,
                                       height=768))
        e.set_thumbnail(url=user["profile_image_url"])

        c = await self.bot.fetch_channel(config.notification_channel)
        emb = await c.send(embed=e)
        return emb


def setup(bot):
    bot.add_cog(TwitchNotifs(bot))
