import discord
import requests

from discord.ext import commands
from discord.ext.commands import *


class mcinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def mcinfo(self, ctx, version=None):
        url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        r = requests.get(url)

        mcversion = r.json()

        if version is None:
            embed = discord.Embed(
                title="Minecraft info",
                description=f"""
Latest release: {mcversion["latest"]['release']}
Latest snapshot: {mcversion["latest"]['snapshot']}
Full release date: <t:1321614000:D> (<t:1321614000:R>)
First went public: <t:1242554400:D> (<t:1242554400:R>)
""")

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(mcinfo(bot))
