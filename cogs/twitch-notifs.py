import re

from discord.ext import commands


class Dev(commands.Cog):
    """Development stuff"""

    def __init__(self, bot):
        self.bot = bot
        self.issue = re.compile(r'##(?P<number>[0-9]+)')

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author) or ctx.author.id == 211238461682876416
        
    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(str(left + right))
def setup(bot):
    bot.add_cog(Dev(bot))