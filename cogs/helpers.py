from typing import Optional

import discord
from discord.ext import commands, flags

from bot import DumbBot


class Helper(commands.Cog):

    helpers = {
        "Python": "<@&828318740756037632>",
        "Javasciprt": "<@&845049397238562927>",
    }

    def __init__(self, bot: DumbBot):
        self.bot = bot

    @commands.command()
    async def helper(self, ctx, helper=None):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        if helper == None:
            await ctx.send(
                embed=discord.Embed(
                    title="Select",
                    description="helper_roles: `{}`".format(i for i in self.helpers),
                )
            )
            res = await self.bot.wait_for("message", check=check, timeout=10)
            if res == "python" or "py":
                await ctx.send(self.helpers["Python"])
            if res == "javascript" or "js":
                await ctx.send(self.helpers["Python"])
            else:
                await ctx.send("Not a valid option ")
        elif helper == "python" or "py":
            await ctx.send(self.helpers["Python"])
        elif helper == "javascript" or "js":
            await ctx.send(self.helpers["Javasciprt"])


def setup(bot: DumbBot):
    bot.add_cog(Helper(bot))
