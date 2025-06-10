import discord
import random
import os
import logging
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
intents.members = True  # Requires privileged intent in Developer Portal
intents.message_content = True  # Required for commands to work

# Initialize bot with prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Event triggered when the bot is ready and connected to Discord."""
    logger.info(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!help for commands"))

@bot.event
async def on_member_join(member):
    """Event triggered when a new member joins the server."""
    try:
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to the server!'
        )
        # Find a general channel to announce the new member
        for channel in member.guild.text_channels:
            if channel.permissions_for(member.guild.me).send_messages:
                await channel.send(f'Welcome {member.mention} to the server!')
                break
    except Exception as e:
        logger.error(f"Error in on_member_join: {e}")

@bot.event
async def on_member_remove(member):
    """Event triggered when a member leaves the server."""
    logger.info(f'{member.name} has left the server')
    # Find a general channel to announce the member leaving
    for channel in member.guild.text_channels:
        if channel.permissions_for(member.guild.me).send_messages:
            await channel.send(f'{member.name} has left the server.')
            break

@bot.event
async def on_command_error(ctx, error):
    """Global error handler for command errors."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"An error occurred: {error}")

# Fun Commands
@bot.command(name="8ball", help="Ask a yes/no question")
async def eight_ball(ctx, *, question):
    """Magic 8-ball command that answers yes/no questions."""
    responses = [
        'Yes',
        'Most likely',
        'Certainly',
        'Without a doubt',
        'Probably',
        'Maybe',
        'Not sure',
        'Unlikely',
        'No',
        'Definitely not'
    ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@bot.command(help="Ask who will do something")
async def who(ctx, *, question):
    """Randomly selects a server member to answer 'who' questions."""
    members = [member.name for member in ctx.guild.members if not member.bot]
    if members:
        await ctx.send(f'Who {question}?\n{random.choice(members)}')
    else:
        await ctx.send("I couldn't find any members to choose from.")

@bot.command(help="Check someone's vibe")
async def vibecheck(ctx, *, subject):
    """Performs a 'vibe check' on the mentioned subject."""
    vibes = [
        'chill',
        'awesome',
        'cool',
        'energetic',
        'relaxed',
        'focused',
        'creative',
        'determined'
    ]
    await ctx.send(f'{subject} is {random.choice(vibes)}')

# Utility Commands
@bot.command(help="Clear messages from the channel")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Clears a specified number of messages from the channel."""
    if amount <= 0:
        await ctx.send("Please provide a positive number of messages to delete.")
        return
    
    if amount > 100:
        await ctx.send("You can only delete up to 100 messages at once.")
        return
        
    await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
    await ctx.send(f"{amount} messages cleared!", delete_after=5)

@bot.command(help="Get information about a user")
async def userinfo(ctx, member: discord.Member = None):
    """Displays information about a user."""
    if member is None:
        member = ctx.author
        
    embed = discord.Embed(
        title=f"User Information - {member.name}",
        color=member.color
    )
    
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Created at", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Joined at", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(help="Get server information")
async def serverinfo(ctx):
    """Displays information about the server."""
    guild = ctx.guild
    
    embed = discord.Embed(
        title=f"Server Information - {guild.name}",
        color=discord.Color.blue()
    )
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Created at", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    
    await ctx.send(embed=embed)

@bot.command(help="Make the bot say something")
async def say(ctx, *, message):
    """Makes the bot say a message."""
    await ctx.message.delete()
    await ctx.send(message)

@bot.command(help="Roll a dice")
async def roll(ctx, dice: str = "1d6"):
    """Rolls dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
        if rolls > 100 or limit > 100:
            await ctx.send("I can't roll that many dice or sides!")
            return
            
        results = [random.randint(1, limit) for _ in range(rolls)]
        await ctx.send(f"Rolling {dice}: {', '.join(map(str, results))}\nTotal: {sum(results)}")
    except Exception:
        await ctx.send("Format has to be NdN (e.g. 1d6, 2d20)")

# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        logger.error("No Discord token found. Please set the DISCORD_TOKEN environment variable.")
        exit(1)
    bot.run(TOKEN)