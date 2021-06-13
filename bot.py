from typing import Iterable

from tortoise import Tortoise, models
from asyncpg.pool import create_pool
import discord
from discord import Color, Embed, utils
from discord.ext import commands, flags, tasks
import models
from models import GuildModel
import re


class DumbBot(commands.AutoShardedBot): 
    def __init__(
        self,
        *,
        tortoise_config: dict,
        prefix: str,
        load_exts: bool = True,
        load_jsk: bool = True
    ):
        self.prefix_cache = {}
        self.tortoise_config = tortoise_config
        super().__init__(
            command_prefix=self.get_bot_prefix,
            intents=discord.Intents.all(),
            shard_count=5
        )

        if load_exts:
            self.load_ext("core")
            self.load_ext("cogs.code_runner")
            self.load_ext("cogs.economy")
            self.load_ext("cogs.rtfm")
            self.load_ext("cogs.helpers")
            self.load_ext("cogs.mod")
            self.load_ext("cogs.events.events")

        if load_jsk:
            self.load_ext("jishaku")

    @tasks.loop(seconds=1)
    async def db(self):
        print("connecting to db...")
        print("-------")
        await Tortoise.init(self.tortoise_config.db_url)
        print("Done!")
        print("-------")
        print("-------")

    def load_ext(self, ext: str):
        try:
            self.load_extension(ext)
        except Exception as e:
            raise e

    async def get_prefix(self, message: discord.Message) -> str:
        if not message.guild:
            return "."
        guild_id = message.guild.id
        if guild_id in self.prefix_cache:
            return self.prefix_cache[guild_id]
        guild, _ = await GuildModel.get_or_create(id=guild_id)
        self.prefix_cache[guild_id] = guild.prefix
        return guild.prefix

    async def get_bot_prefix(self,message: discord.Message) -> str:
        prefix = await self.fetch_prefix(message)
        bot_id = self.user.id
        prefixes = [prefix,f"<@{bot_id}>", f"<@!{bot_id}>"]
        regex = re.compile(
            "^(" + "|".join(re.escape(p) for p in prefixes) + ").*", flags=re.I
        )
        matches = regex.match(message.content)
        if matches is not None:
            return matches.group(1)
        else:
            return prefix

    async def on_ready(self):
        print("ready")
        print("connecting to db...")
        print("-------")
        await Tortoise.init(db_url="sqlite://db.sqlite3",
                            modules={'models': ["models"]}
                                                            )
        await Tortoise.generate_schemas()
        print("Done!")
        print("-------")
        print("-------")
