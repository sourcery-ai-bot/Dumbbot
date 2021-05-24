import discord
from discord import Color, Embed, utils
from discord.ext import commands, flags, tasks

from bot import DumbBot


class Common(commands.Cog):
    def __init__(self, bot: DumbBot):
        self.bot = bot

    @commands.command(aliases=["latency"], name="ping")
    async def ping(self, ctx):
        """Check latency of the bot"""
        latency = str(round(self.bot.latency * 1000, 1))
        await ctx.send(
            embed=Embed(title="Pong!", description=f"{latency}ms", color=Color.blue())
        )

    @commands.command()
    async def stats(self, ctx):
        fields = (
            ("Guilds", "{}".format(len(self.bot.guilds))),
            ("Users", "{}".format(len(self.bot.users))),
            ("Python_Version", "{}".format("3.9.5")),
            ("Discord.py_Version", "{}".format("1.7.2")),
        )
        embed = Embed(color=ctx.author.color)
        for i, e in fields:
            embed.add_field(name=i, value=e, inline=False)

        await ctx.send(embed=embed)


def setup(bot: DumbBot):
    bot.add_cog(Common(bot))
