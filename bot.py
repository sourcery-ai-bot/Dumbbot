from typing import Iterable

from asyncpg.pool import create_pool
import discord
from discord import Color, Embed, utils
from discord.ext import commands, flags, tasks

class DumbBot(commands.Bot): 
    def __init__(
        self,
        *,
        tortoise_config: dict,
        prefix: str,
        load_exts: bool = True,
        load_jsk: bool = True
    ):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
        )
        def load_exts_(exts: str):
            for ext in exts:
                try:
                    self.load_extension(ext)
                except Exception as e:
                    raise e

        if load_exts:
            try:
                self.load_extension("core")
                self.load_extension("cogs.fun")
                self.load_extension("cogs.code_runner")
                self.load_extension("cogs.economy")
                self.load_extension("cogs.rtfm")
                self.load_extension("cogs.helpers")
                self.load_extension("cogs.mod")
                self.load_extension("cogs.events.events")
            except Exception as theerror:
                raise theerror

    async def on_ready(self):
        print("ready")
