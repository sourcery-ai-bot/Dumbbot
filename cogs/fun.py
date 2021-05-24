import asyncio

import discord
from discord import Color, Embed, Member, utils
from discord.ext import commands, flags, tasks

from bot import DumbBot


class Fun(commands.Cog):
    def __init__(self, bot: DumbBot):
        self.bot = bot

    @commands.command()
    async def coffee(self, ctx, user: Member = None):
        if user == None:
            await ctx.send("{} coffeeeeee!!!".format(ctx.author.name))
        if user.bot:
            return await ctx.send(
                "yeahh..... coffee with bots isn't really a thing......."
            )
        else:
            await ctx.send("{},{} Enjoy the Coffee".format(ctx.author.name, user.name))

    @commands.command(aliases=["coffeeparty"])
    async def coffee_party(self, ctx, *, reason: str = None):
        r = "\nReason: " + reason if reason else "None"
        my_message = await ctx.send("coffee party is hosted!\n reason: {}".format(r))
        await my_message.add_reaction("☕")
        await asyncio.sleep(10)
        members = (
            await (await ctx.channel.fetch_message(my_message.id))
            .reactions[0]
            .users()
            .flatten()
        )
        await ctx.send(
            "{}, Enjoy".format(
                [
                    utils.escape_mentions(member.display_name)
                    for member in members
                    + ([] if ctx.author in members else [ctx.author])
                    if not member.bot
                ]
            )
        )

    @commands.command()
    async def add(self, ctx, num1: int, num2: int):
        try:
            result = "{}".format(num1 + num2)
            await ctx.send(
                embed=Embed(title="Added", description="Answer: {}".format(result))
            )
        except ValueError:
            await ctx.send("that was not a number")

    @commands.command()
    async def remove(self, ctx, num1: int, num2: int):
        try:
            result = "{}".format(num1 - num2)
            await ctx.send(
                embed=Embed(title="Removed", description="Answer: {}".format(result))
            )
        except ValueError:
            await ctx.send("That was not a numer")

    @commands.command()
    async def multiply(self, ctx, num1: int, num2: int):
        try:
            result = "{}".format(num1 * num2)
            await ctx.send(
                embed=Embed(title="Multiplied", description="Answer: {}".format(result))
            )
        except ValueError:
            await ctx.send("That was not a numer")

    @commands.command()
    async def divide(self, ctx, num1: int, num2: int):
        try:
            result = "{}".format(num1 / num2)
            await ctx.send(
                embed=Embed(title="Dvided", description="Answer: {}".format(result))
            )
        except ValueError:
            await ctx.send("That was not a numer")


def setup(bot: DumbBot):
    bot.add_cog(Fun(bot))
