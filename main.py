import os
import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('discord_bot')

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents
intents = discord.Intents.default()
# Note: You need to enable these privileged intents in the Discord Developer Portal
# at https://discord.com/developers/applications/
# For now, we'll disable them to make the bot work immediately
intents.members = False  # Requires privileged intent in Developer Portal
intents.message_content = True  # Required for commands to work

# Initialize bot with prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: {filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load extension {filename[:-3]}: {e}')

@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} has connected to Discord!')
    logger.info(f'Bot ID: {bot.user.id}')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')

# Run the bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    if not TOKEN:
        logger.error("No Discord token found. Please set the DISCORD_TOKEN environment variable.")
        exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown by user")
    except Exception as e:
        logger.error(f"Error: {e}")