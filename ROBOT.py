import discord
import itertools

from discord.ext  import commands
from discord.http import asyncio
from json         import load
from time         import time

# Sets up the configuration
configFile = open("setup.json")
configuration = load(configFile)

BOT_TOKEN = configuration.get("token")
DEFAULT_ACTIVITY = discord.Game(name=configuration.get("activity"))
COGS = configuration.get("cogs")
PREFIXES = configuration.get("prefixes")
WEBHOOK_ID = configuration.get("webhook")
WEBHOOK_TOKEN = configuration.get("webhook-token")
EMBED_COLOR = int(configuration.get("color"))

# Establishes the bot
bot = commands.Bot(command_prefix=PREFIXES, case_insensitive=True, activity=DEFAULT_ACTIVITY, owner_id = 156021301654454272)

# Loads the modules of the bot
if __name__ == "__main__":
    for cog in COGS:
        bot.load_extension(cog)

# Allows for the code to be reloaded without reloading the bot
@bot.command()
@commands.is_owner()
async def reloadcog(ctx, cog: str):
    if cog == "all":
        extensions = [a for a in bot.extensions.keys()]
        for extension in extensions:
            bot.reload_extension(extension)
        await ctx.send("Reloaded all extensions.")
    elif cog in bot.extensions.keys():
        bot.reload_extension(cog)
        await ctx.send("Reloaded extension.")
    

bot.run(BOT_TOKEN, bot = True, reconnect = True)