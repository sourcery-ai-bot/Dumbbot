from typing import Iterable

from asyncpg.pool import create_pool
import discord
from discord import Color, Embed, utils
from discord.ext import commands, flags, tasks


class DumbBot(commands.AutoShardedBot): 
    def __init__(
        self,
        *,
        tortoise_config: dict,
        prefix: str,
        load_exts: bool = True,
        load_jsk: bool = True
    ):
        super().__init__(
            command_prefix=prefix,
            intents=discord.Intents.all(),
            shard_count=5
        )

        if load_exts:
            self.load_ext("core")
            self.load_ext("cogs.fun")
            self.load_ext("cogs.code_runner")
            self.load_ext("cogs.economy")
            self.load_ext("cogs.rtfm")
            self.load_ext("cogs.helpers")
            self.load_ext("cogs.mod")
            self.load_ext("cogs.tags")
            self.load_ext("cogs.events.events")

        if load_jsk:
            self.load_ext("jishaku")


    def load_ext(self, ext: str):
        try:
            self.load_extension(ext)
        except Exception as e:
            raise e


    async def on_ready(self):
        print("ready")
