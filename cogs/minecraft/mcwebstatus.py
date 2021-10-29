import discord
import requests

from discord.ext import commands
from discord.ext.commands import *


class mcstatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def mcstatus(self, ctx):
        message = await ctx.reply("Geting statuses from the websites... <a:loading:894950036964782141>")

        mc_sites = [
            "minecraft.net",                         # Main website
            "mojang.com",                            # Mojang website, used to change information about mojang accounts
            "session.minecraft.net",                 # Possibly deprecated
            "authserver.mojang.com",
            "account.mojang.com",
            "api.mojang.com",
            "textures.minecraft.net",                # Texture assets
            "launchermeta.mojang.com",               # Stores hashes in a json file, to use later to get assets
            "libraries.minecraft.net",               # Used for minecraft libraries
            "sessionserver.mojang.com",
            "api.minecraftservices.com",             # Unsure what this is used for
            "resources.download.minecraft.net",      # Used to get minecraft resources
            "launcher.mojang.com"                    # Used to get version.jar (does not get assets?)
        ]

        embed_desc = ""

        for url in mc_sites:
            try:
                r = requests.head(f"https://{url}", timeout=2)

                if r.ok:
                    embed_desc += f"**{url}:**\n<:Green:894954521724350485> {r.status_code} {r.reason}.\n"
                else:
                    embed_desc += f"**{url}:**\n<:Yellow:894954521674018877> {r.status_code} {r.reason}.\n"

            except requests.exceptions.Timeout as error:
                embed_desc += f"**{url}:**\n<:Red:894954521862766642> Timed out.\n"
            except requests.exceptions.RequestException as error:
                embed_desc += f"**{url}:**\n<:Red:894954521862766642> There was an error. Error: {error.response}\n"

            embed = discord.Embed(title="Responses from the different minecraft related websites.", description=embed_desc)
            embed.set_footer(text=f"Command executed by: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            await message.edit(embed=embed)
        await message.edit("")


def setup(bot):
    bot.add_cog(mcstatus(bot))
