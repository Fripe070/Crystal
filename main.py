import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from functions import getcogs

bot = commands.Bot(
    command_prefix="c!",
    strip_after_prefix=True,
    case_insensitive=True
)

for cog in getcogs():
    try:
        bot.load_extension(cog.replace('\\', '.').replace('/', '.'))
        print(cog)
    except Exception as error:
        print(error)


@bot.event
async def on_ready():
    print("e")

load_dotenv()
bot.run(os.getenv('TOKEN'))
