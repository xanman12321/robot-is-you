import discord
import logging

from json        import load
from discord.ext import commands

# Sets up logging 
logging.basicConfig(filename="log.txt", level=20, format="%(asctime)s - %(levelname)s - %(message)s") 

# Sets up the configuration
configFile = open("setup.json")
configuration = load(configFile)

BOT_TOKEN = configuration.get("token")
DEFAULT_ACTIVITY = discord.Game(name=configuration.get("activity"))
COGS = configuration.get("cogs")

# Establishes the bot
bot = commands.Bot(command_prefix=["+"], case_insensitive=True, help_command=None)

# Loads the modules of the bot
if __name__ == "__main__":
    for cog in COGS:
        bot.load_extension(cog)

# Basic bot events
@bot.event
async def on_connect():
    logging.info("Connected to Discord.")

@bot.event
async def on_ready():
    logging.info("Client caches filled. Ready.")

bot.run(BOT_TOKEN, bot = True, reconnect = True)