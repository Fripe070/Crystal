import discord
import requests

from discord.ext import commands
from discord.ext.commands import *


class mcserverping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def mcserver(self, ctx, ip=None, port=None):
        if ip is None:
            await ctx.reply("You have to specify a server ip.")
            return

        url = f"https://api.mcsrvstat.us/2/{ip}"

        if port is not None:
            url += f":{port}"

        r = requests.get(url)
        server = r.json()

        if server["online"] is False:
            if port:
                await ctx.reply("Server is currently offline, did you use the correct port?")
            else:
                await ctx.reply("Server is currently offline.")
            return

        motd = ""
        for i in server["motd"]["clean"]:
            motd += i.strip() + "\n"

        embed_desc = f"""
**Server ip:** \"{server["hostname"]}\" ({server["ip"]})
**Port:** `{server["port"]}`

**Version:** {server['version']}
**Players:** {server['players']['online']}/{server['players']['max']}
"""
        try:
            embed_desc += f"**Software:** {server['software']}\n"
        except KeyError:
            pass

        try:
            embed_desc += f"**Current map:** {server['map']}\n"
        except KeyError:
            pass

        embed_desc += f"""
**Motd:** ```
{motd}
```
"""

        embed = discord.Embed(
            title=f'Info about server "{ip}"',
            description=embed_desc
        )

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(mcserverping(bot))
