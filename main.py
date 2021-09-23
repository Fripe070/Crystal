import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(
    command_prefix="c!",
    strip_after_prefix=True,
    case_insensitive=True
)


@bot.event
async def on_ready():
    print("e")

load_dotenv()
bot.run(os.getenv('TOKEN'))
