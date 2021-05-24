import os

import discord
from discord.ext import commands

from bot import DumbBot


class Events(commands.Cog):
    def __init__(self, bot: DumbBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"Sorry you are not allowed to use this command, {ctx.author.mention}."
            )
            return
        if isinstance(error, commands.CommandOnCooldown):
            msg = "**Still on cooldown**, please try again in {:.2f}s".format(
                error.retry_after
            )
            await ctx.send(msg)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(str(error))
            return
        else:
            raise error


def setup(bot: DumbBot):
    bot.add_cog(Events(bot))
