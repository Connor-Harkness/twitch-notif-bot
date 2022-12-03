# This example requires the 'members' privileged intent to use the Member converter
# and the 'message_content' privileged intent for prefixed commands.

import random
import config
import sys, traceback
import datetime
from cogs.utils import context

import discord
from discord.ext import commands

description = """
An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class Twitch_Notif_Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            description=description,
            intents=intents,
            )
        self.load_cogs()
    def load_cogs(self):
        for cog in config.base_cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f"Cog '{cog}' failed to load.", file=sys.stderr)
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
            print(f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)

    @property
    def config(self):
        return config

    def run(self):
        super().run(config.token)
if __name__ == '__main__':
    twitch_notif_bot = Twitch_Notif_Bot()
    twitch_notif_bot.run()
# @bot.command()
# async def add(ctx: commands.Context, left: int, right: int):
#     """Adds two numbers together."""
#     await ctx.send(str(left + right))


# @bot.command()
# async def roll(ctx: commands.Context, dice: str):
#     """Rolls a die in NdN format."""
#     try:
#         rolls, limit = map(int, dice.split("d"))
#     except ValueError:
#         await ctx.send("Format has to be in NdN!")
#         return

#     # _ is used in the generation of our result as we don't need the number that comes from the usage of range(rolls).
#     result = ", ".join(str(random.randint(1, limit)) for _ in range(rolls))
#     await ctx.send(result)


# @bot.command(description="For when you wanna settle the score some other way")
# async def choose(ctx: commands.Context, *choices: str):
#     """Chooses between multiple choices."""
#     await ctx.send(random.choice(choices))


# @bot.command()
# async def repeat(ctx: commands.Context, times: int, *, content: str = "repeating..."):
#     """Repeats a message multiple times."""
#     for _ in range(times):
#         await ctx.send(content)


# @bot.command()
# async def joined(ctx: commands.Context, member: discord.Member):
#     if member:
#         """Says when a member joined."""
#         await ctx.send(f"{member.name} joined in {member.joined_at}")
#     else:
#         await ctx.send(f"Failed cause of no member, member actually is: {member}")


# @bot.group()
# async def cool(ctx: commands.Context):
#     """
#     Says if a user is cool.

#     In reality this just checks if a subcommand is being invoked.
#     """

#     if ctx.invoked_subcommand is None:
#         await ctx.send(f"No, {ctx.subcommand_passed} is not cool")


# @cool.command(name="bot")
# async def _bot(ctx: commands.Context):
#     """Is the bot cool?"""
#     await ctx.send("Yes, the bot is cool.")


# bot.run(config.token)