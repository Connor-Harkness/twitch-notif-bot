import config
import sys
import traceback
import datetime
from cogs.utils import context

import discord
from discord.ext import commands

description = """
Twitch notification bot for Discord
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class Twitch_Notif_Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.prefix),
            description=description,
            intents=intents,
        )
        self.load_cogs()

    def load_cogs(self):
        for cog in config.base_cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f"Cog '{cog}' failed to load.\n{e}", file=sys.stderr)
                traceback.print_exc()

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        print(f'Ready: {self.user} (ID: {self.user.id})')
        print(f'Discord {discord.__version__}')

    async def on_resumed(self):
        print('Resumed..')

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=context.Context)

        if ctx.command is None:
            return

        await self.invoke(ctx)

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        # TODO: Add extra error handling
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command is only for use inside guilds.')
        elif isinstance(error, commands.DisabledCommand):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Please wait before using this command again.")
        elif isinstance(error, commands.CommandInvokeError):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(
                f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)

    @property
    def config(self):
        return config

    def run(self):
        super().run(config.token)


if __name__ == '__main__':
    twitch_notif_bot = Twitch_Notif_Bot()
    twitch_notif_bot.run()
