import asyncio
import discord
import jishaku
import logging
import sys

from datetime     import datetime
from discord.ext  import commands
from json         import load

logging.basicConfig(filename="log.txt", level=logging.WARNING)

# Sets up the configuration
configuration = None
with open("setup.json") as config_file:
    configuration = load(config_file)

BOT_TOKEN = configuration.get("token")
DBL_TOKEN = configuration.get("dbl") or ""
DEFAULT_ACTIVITY = discord.Game(name=configuration.get("activity"))
COGS = configuration.get("cogs")
PREFIXES = configuration.get("prefixes")
PREFIXES_MENTION = commands.when_mentioned_or(*PREFIXES) if configuration.get("mention") else PREFIXES
WEBHOOK_ID = configuration.get("webhook")
EMBED_COLOR = configuration.get("color")
VANILLA = configuration.get("vanilla")

# Uses a custom bot class
class BabaBot(commands.Bot):
    def __init__(self, command_prefix, webhook_id, embed_color, vanilla, help_command=None, description=None, top=None, **options):
        self.loading = False
        self.started = datetime.utcnow()
        self.vanilla_only = bool(vanilla)
        self.embed_color = embed_color
        self.webhook_id = webhook_id
        self._top = top
        super().__init__(command_prefix, help_command=help_command, description=description, **options)
    
    # Custom send that sends content in an embed
    # Note that due to AllowedMentions, mentions do not have to be "sanitized"
    async def send(self, ctx, content, embed=None, tts=False, file=None):
        if len(content) > 2000:
            content = content[:1963] + " [...] \n\n (Character limit reached!)"
        if embed is not None:
            return await ctx.send(content, embed=embed)
        segments = content.split("\n")
        title = segments[0]
        description="\n".join(segments[1:])
        if len(title) > 256:
            title = None
            description = "\n".join(segments)
        container = discord.Embed(title=title, description=description, color=self.embed_color)
        await ctx.send(embed=container, tts=tts, file=file)

    # Custom error message implementation
    # Sends the error message. Automatically deletes it after some time.
    async def error(self, ctx, title, content=None):
        _title = f"{title}"
        description = content if content else None
        embed = discord.Embed(
            title=_title, 
            description=description,
            color=self.embed_color
        )
        await ctx.message.add_reaction("⚠️")
        await ctx.send(embed=embed, delete_after=20)

# Requires discord.py v1.4+
default_mentions = discord.AllowedMentions(everyone=False, roles=False)

# Establishes the bot
bot = BabaBot(
    # Prefixes
    PREFIXES_MENTION,
    # Logger
    WEBHOOK_ID, 
    # Misc values
    EMBED_COLOR, 
    VANILLA, 
    top=DBL_TOKEN,
    # Other behavior parameters
    case_insensitive=True, 
    activity=DEFAULT_ACTIVITY, 
    owner_id = 156021301654454272,
    description="*An entertainment bot for rendering levels and custom scenes based on the indie game Baba Is You.*",
    # Never mention roles or @everyone / @here
    allowed_mentions=default_mentions, 
    # Disable the member cache
    fetch_offline_members=False,
    # Disable presence updates 
    guild_subscriptions=False,
    # Disable message cache
    max_messages=None
)

bot.prefixes = PREFIXES
bot.exit_code = 0

# Loads the modules of the bot
if __name__ == "__main__":
    for cog in COGS:
        bot.load_extension(cog)

bot.run(BOT_TOKEN, bot = True, reconnect = True)

sys.exit(bot.exit_code)