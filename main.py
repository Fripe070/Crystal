import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

prefix = ["c!"]

bot = commands.Bot(
    command_prefix=prefix,
    strip_after_prefix=True,
    case_insensitive=True
)


@bot.event
async def on_ready():
    print("e")

load_dotenv()
bot.run(os.getenv('TOKEN'))
