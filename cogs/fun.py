import asyncio

import aiohttp
import discord
from discord import Color, Embed, Member, utils
from discord.ext import commands, flags, tasks

from bot import DumbBot


class Fun(commands.Cog):
    def __init__(self, bot: DumbBot):
        self.bot = bot

    @commands.command()
    async def coffee(self, ctx, user: Member = None):
        if user is None:
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

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.bot.http._HTTPClient__session

    async def find_pkg(self, arg: str):
        return await self.session.get(
            "https://pypi.org/pypi/{module}/json".format(module=arg) # for this we will use the endpoints of pypi.org
        )
"""
The pypi command is taken and modified from https://github.com/TechStruck/TechStruck-Bot/blob/main/bot/cogs/pypi.py
"""
    @commands.command()
    async def pypi(self, ctx, pkg: str):
        pypi_response = await self.find_pkg(pkg)
        try:
            pypi_json = await pypi_response.json()
        except:
            await ctx.send("No module named {} was not found".format(pkg))

        result = pypi_json["info"]

        def getval(key):
            return result[key] or "Unknown"

        name = getval("name")
        author = getval("author")
        project_url = getval("project_url")
        _license = getval("license")
        description = getval("summary")
        home_page = getval("home_page")
        embed = discord.Embed(
            description=f"[**{name}**]({home_page})", color=ctx.author.color
        )
        embed.add_field(name="Author", value=author)
        embed.add_field(name="license", value=_license, inline=False)
        embed.add_field(name="Summary", value=description)
        embed.add_field(name="Project url", value=project_url, inline=False)
        embed.add_field(name="Home Page", value=home_page)
        await ctx.send(embed=embed)


def setup(bot: DumbBot):
    bot.add_cog(Fun(bot))
