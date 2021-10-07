import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(
    command_prefix="c!",
    strip_after_prefix=True,
    case_insensitive=True
)

# Error handler
@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.NotOwner):
        await ctx.reply("You do not have the needed permissions to execute this command!")
    elif isinstance(err, commands.MissingPermissions):
        await ctx.reply("You do not have the needed permissions to execute this command!")
    else:
        try:
            embed = discord.Embed(title="An error occurred!", description=f"{err}", colour=0xCC1818)
            await ctx.send(embed=embed)
        except Exception as e:  # If bot can't send error message
            print("Couldn't send error message!")
            print(e)

@bot.event
async def on_ready():
    print("e")

load_dotenv()
bot.run(os.getenv('TOKEN'))
