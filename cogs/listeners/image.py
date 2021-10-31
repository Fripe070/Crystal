import discord

from discord.ext import commands
from discord.ext.commands import *

from io import BytesIO
from cairosvg import svg2png


class image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            for attachment in ctx.attachments:
                if not attachment.is_spoiler():
                    if attachment.content_type.startswith("image/svg"):
                        f = BytesIO(svg2png(url=attachment.url, output_width=1024, output_height=1024))

                        await ctx.reply(file=discord.File(f, filename=f"{attachment.filename}.png"), mention_author=False)


def setup(bot):
    bot.add_cog(image(bot))
