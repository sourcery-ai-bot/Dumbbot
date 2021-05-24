import os

from discord import Color, Embed

from bot import *


class Help_Command(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for e in self.paginator.pages:
            em = discord.Embed(description=e, color=Color.greyple())
            await destination.send(embed=em)


if __name__ == "__main__":
    from config.bot import *

    client = DumbBot(
        tortoise_config=bot_config,
        prefix=bot_config.prefix,
    )
    client.help_command = Help_Command()
    client.run(bot_config.token)
