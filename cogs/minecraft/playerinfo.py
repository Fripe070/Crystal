import discord
import requests
import base64
import json
import os
import time

from discord.ext import commands
from discord.ext.commands import *
from dotenv import load_dotenv

load_dotenv()
hypixel_api_key = os.getenv('HYPIXEL_API_KEY')


class playerinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['mcplayer', 'mcuser', "mcusr"])
    async def playerinfo(self, ctx, player):
        await ctx.message.add_reaction("<a:loading:894950036964782141>")
        msg = await ctx.send("Fetching player UUID... (this might take a while)")

        url = f"https://api.mojang.com/users/profiles/minecraft/{player}"

        try:
            uuid = requests.get(url).json()["id"]
        except Exception:
            if requests.get(f"https://api.mojang.com/user/profiles/{player}/names"):
                uuid = player
            else:
                await ctx.reply("That username is not taken.")
                return

        await msg.edit(content="Fetching player names... (this might take a while)")

        url = f"https://api.mojang.com/user/profiles/{uuid}/names"
        tmprequest = requests.get(url).json()

        pastnames = []

        for name in tmprequest:
            try:
                pastnames.append(f"{name['name']} (<t:{int(int(name['changedToAt']) / 1000)}:R>)")
            except Exception:
                try:
                    pastnames.append(f"{name['name']} (original)")
                except Exception:
                    pass

        pastnames.reverse()
        pastnames = ", \n".join(pastnames)

        if len(pastnames) > 1020:
            pastnames = pastnames[:1020] + "..."

        await msg.edit(content="Fetching player model info... (this might take a while)")

        url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        tmprequest = requests.get(url).json()

        skincape = tmprequest["properties"][0]["value"]

        skincape = json.loads(base64.b64decode(skincape).decode("utf-8"))

        username = tmprequest["name"]

        await msg.edit(content="Fetching player model type... (this might take a while)")
        try:
            if skincape["textures"]["SKIN"]["metadata"] == {"model": "slim"}:
                playermodel = "Slim"
            else:
                playermodel = "Classic"
        except KeyError:
            playermodel = "Classic"

        embed_desc = f"**Player name:** {username}\n**UUID:** `{uuid}`\n\n**Player model:** {playermodel}\n"

        await msg.edit(content="Fetching player skin... (this might take a while)")
        if "SKIN" in skincape["textures"]:
            embed_desc += f'**Skin:** [link]({skincape["textures"]["SKIN"]["url"]})\n'

        await msg.edit(content="Fetching player cape... (this might take a while)")
        if "CAPE" in skincape["textures"]:
            cape_url = skincape["textures"]["CAPE"]["url"]
            migrator = "2340c0e03dd24a11b15a8b33c2a7e9e32abb2051b2481d0ba7defd635ca7a933"
            minecon11 = "953cac8b779fe41383e675ee2b86071a71658f2180f56fbce8aa315ea70e2ed6"
            minecon12 = "a2e8d97ec79100e90a75d369d1b3ba81273c4f82bc1b737e934eed4a854be1b6"
            minecon13 = "153b1a0dfcbae953cdeb6f2c2bf6bf79943239b1372780da44bcbb29273131da"
            minecon15 = "b0cc08840700447322d953a02b965f1d65a13a603bf64b17c803c21446fe1635"
            minecon16 = "e7dfea16dc83c97df01a12fabbd1216359c0cd0ea42f9999b6e97c584963e980"
            realmsmapmaker = "17912790ff164b93196f08ba71d0e62129304776d0f347334f8a6eae509f8a56"
            mojang = "5786fe99be377dfb6858859f926c4dbc995751e91cee373468c5fbf4865e7151"
            translator = "1bf91499701404e21bd46b0191d63239a4ef76ebde88d27e4d430ac211df681e"
            mojangclassic = "8f120319222a9f4a104e2f5cb97b2cda93199a2ee9e1585cb8d09d6f687cb761"
            mojangstudios = "9e507afc56359978a3eb3e32367042b853cddd0995d17d0da995662913fb00f7"
            mojira = "ae677f7d98ac70a533713518416df4452fe5700365c09cf45d0d156ea9396551"



            if cape_url.endswith(migrator):
                embed_desc += '**Cape:** [migrator]'
            elif cape_url.endswith(minecon11):
                embed_desc += '**Cape:** [MineCon 2011]'
            elif cape_url.endswith(minecon12):
                embed_desc += '**Cape:** [MineCon 2012]'
            elif cape_url.endswith(minecon13):
                embed_desc += '**Cape:** [MineCon 2013]'
            elif cape_url.endswith(minecon15):
                embed_desc += '**Cape:** [MineCon 2015]'
            elif cape_url.endswith(minecon16):
                embed_desc += '**Cape:** [MineCon 2016]'
            elif cape_url.endswith(realmsmapmaker):
                embed_desc += '**Cape:** [Realms Mapmaker]'
            elif cape_url.endswith(mojang):
                embed_desc += '**Cape:** [Mojang]'
            elif cape_url.endswith(mojangclassic):
                embed_desc += '**Cape:** [Mojang (Classic)]'
            elif cape_url.endswith(mojangstudios):
                embed_desc += '**Cape:** [Mojang Studios]'
            elif cape_url.endswith(translator):
                embed_desc += '**Cape:** [Translator]'
            elif cape_url.endswith(mojira):
                embed_desc += '**Cape:** [Mojira Moderator]'
            else:
                embed_desc += f'**Cape:** [Other]'

            embed_desc += f'({skincape["textures"]["CAPE"]["url"]})\n'

        await msg.edit(content="Applying embed description... (this might take a while)")
        embed = discord.Embed(
            title=f'Minecraft user information for player "{username}"',
            description=embed_desc
        )

        await msg.edit(content="Applying embed thumbnail... (this might take a while)")
        try:
            embed.set_thumbnail(url=f"https://crafatar.com/renders/body/{uuid}?overlay")
        except KeyError:
            pass

        embed.add_field(name="Name history:", value=pastnames)
        embed.set_footer(text=f"Command executed by: {ctx.author.display_name}")

        await msg.edit(content="Fetching player info from the hypixel API... (this might take a while)")
        try:
            # HYPIXEL
            url = f"https://api.slothpixel.me/api/players/{uuid}"
            hypixel = requests.get(url).json()

            if hypixel['online']:
                last_seen = "Now"
            else:
                if hypixel['last_logout']:
                    last_seen = f"<t:{round(hypixel['last_logout']/1000)}:R>"
                else:
                    last_seen = None

            status = f"""{'Online' if hypixel['online'] else 'Offline'} \
    {'since ' + last_seen if last_seen is not None and not hypixel['online'] else ''}"""

            url = f"https://api.slothpixel.me/api/players/{uuid}/status"
            playing = requests.get(url).json()['game']['type'] if hypixel['online'] else None

            embed.add_field(
                name="Hypixel:",
                value=f"""**Status:** {status}
**Currectly playing:** {playing if hypixel['online'] and playing is not None else 'Nothing'}
**Rank:** {hypixel['rank'].replace('_PLUS', '+') if hypixel['rank'] else ''}
**Level:** {int(hypixel['level']):,}
**Exp:** {hypixel['exp']:,}
**Total coins:** {hypixel['total_coins']:,}
**Karma:** {hypixel['karma']:,}
**Mc version:** {hypixel['mc_version'] if hypixel['mc_version'] else 'Unknown'}""")
        except KeyError:
            pass
        await msg.delete()
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(playerinfo(bot))
