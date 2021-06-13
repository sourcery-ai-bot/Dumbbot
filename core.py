import discord
from discord import Color, Embed, utils
from discord.ext import commands, flags, tasks

from models import GuildModel
from bot import DumbBot


class Common(commands.Cog):
    def __init__(self, bot: commands.Bot):
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

    @commands.command()
    async def prefix(self, ctx, prefix):
        if len(prefix) > 5:
            await ctx.send("Your prefix can't be longer than 5 charaters!")
            return
        else:
            self.bot.prefix_cache[ctx.guild.id] = prefix
            await GuildModel.filter(id=ctx.guild.id).update(prefix=prefix)
            await ctx.send(f"My prefix has been set to {prefix}")


def setup(bot: commands.Bot):
    bot.add_cog(Common(bot))
