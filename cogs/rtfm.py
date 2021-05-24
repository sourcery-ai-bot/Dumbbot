import warnings

import aiohttp
from discord import Color, Embed
from discord.ext import commands, flags

from bot import DumbBot
from utils import fuzzy, rtfm

"""
Directly taken and modified from TechStruck/TechStruck-Bot
https://github.com/TechStruck/TechStruck-Bot
This code is under the MIT License
"""


class RTFM(commands.Cog):
    """Search through manuals of several python modules and python itself"""

    targets = {
        "python": "https://docs.python.org/3",
        "discord.py": "https://discordpy.readthedocs.io/en/latest",
    }

    aliases = {
        ("py", "py3", "python3", "python"): "python",
        ("dpy", "discord.py", "discordpy"): "discord.py",
    }

    url_overrides = {
        "tensorflow": "https://github.com/mr-ubik/tensorflow-intersphinx/raw/master/tf2_py_objects.inv"
    }

    def __init__(self, bot: DumbBot) -> None:
        self.bot = bot
        self.cache = {}

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.bot.http._HTTPClient__session  # type: ignore

    async def build(self, target) -> None:
        url = self.targets[target]
        req = await self.session.get(
            self.url_overrides.get(target, url + "/objects.inv")
        )
        if req.status != 200:
            warnings.warn(
                Warning(
                    f"Received response with status code {req.status} when trying to build RTFM cache for {target} through {url}/objects.inv"
                )
            )
            raise commands.CommandError("Failed to build RTFM cache")
        self.cache[target] = rtfm.SphinxObjectFileReader(
            await req.read()
        ).parse_object_inv(url)

    @commands.group(invoke_without_command=True)
    async def rtfm(self, ctx: commands.Context, doc: str, *, term: str):
        """
        Search through docs of a module/python
        Args: target, term
        """
        doc = doc.lower()
        target = None
        for aliases, target_name in self.aliases.items():
            if doc in aliases:
                target = target_name

        if not target:
            return await ctx.reply("Alias/target not found")

        cache = self.cache.get(target)
        if not cache:
            await ctx.trigger_typing()
            await self.build(target)
            cache = self.cache.get(target)

        results = fuzzy.finder(term, list(cache.items()), key=lambda x: x[0], lazy=False)[:3]  # type: ignore

        if not results:
            return await ctx.reply("Couldn't find any results")

        await ctx.reply(
            embed=Embed(
                title=f"Searched in {target}",
                description="\n".join([f"[`{key}`]({url})" for key, url in results]),
                color=Color.dark_purple(),
            )
        )

    @rtfm.command(name="list")
    async def list_targets(self, ctx: commands.Context):
        """List all the avaliable documentation search targets"""
        aliases = {v: k for k, v in self.aliases.items()}
        embed = Embed(title="RTFM list of avaliable modules", color=Color.green())
        embed.description = "\n".join(
            [
                "[{0}]({1}): {2}".format(
                    target,
                    link,
                    "\u2800".join([f"`{i}`" for i in aliases[target] if i != target]),
                )
                for target, link in self.targets.items()
            ]
        )

        await ctx.send(embed=embed)


def setup(bot: DumbBot):
    bot.add_cog(RTFM(bot))
