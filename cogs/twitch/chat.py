import json
import time
from datetime import timedelta

from discord.ext import commands


class TwitchChat(commands.Cog):
    """Twitch livestream notifications"""

    def __init__(self, bot):
        self.bot = bot
        self.api = bot.get_cog("TwitchApi")
        self.chat = self.api.chat
        self.connect()
        

    def connect(self):
        self.chat.subscribe(
         lambda message: print(f"{message.channel}><{message.user.display_name}><{message.text}>"))

    
    @commands.command(name="msg")
    async def send_message(self, ctx, *msg):
        # print(" ".join(msg))
        self.chat.send("".join(msg))

    def cog_unload(self):
        pass
def setup(bot):
    bot.add_cog(TwitchChat(bot))
