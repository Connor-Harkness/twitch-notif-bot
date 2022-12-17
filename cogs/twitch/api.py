from datetime import timedelta

import twitch
from discord.ext import commands

import config


class TwitchApi(commands.Cog):
    """Twitch livestream notifications"""

    def __init__(self, bot):
        self.bot = bot
        self.connect()

    def connect(self):
        self.helix = twitch.Helix(config.twitch_client_id, config.twitch_client_secret, use_cache=True,
                                  cache_duration=timedelta(minutes=10))
        self.chat = twitch.Chat(channel=config.twitch_chat_channel, nickname=config.twitch_chat_nickname, oauth=config.twitch_client_oauth, helix=self.helix)
    def cog_unload(self):
        pass

def setup(bot):
    bot.add_cog(TwitchApi(bot))