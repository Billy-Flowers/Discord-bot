import discord
import logging
from discord.ext import commands

logger = logging.getLogger('discord_bot')

class Events(commands.Cog):
    """Event handlers for the bot"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Event triggered when the bot is ready and connected to Discord."""
        logger.info(f'{self.bot.user.name} has connected to Discord!')
        await self.bot.change_presence(activity=discord.Game(name="!help for commands"))
    
    # Note: These events require the members privileged intent to be enabled
    # in the Discord Developer Portal.
    @commands.Cog.listener()
    async def on_member_join(self, member):
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
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Event triggered when a member leaves the server."""
        logger.info(f'{member.name} has left the server')
        # Find a general channel to announce the member leaving
        for channel in member.guild.text_channels:
            if channel.permissions_for(member.guild.me).send_messages:
                await channel.send(f'{member.name} has left the server.')
                break
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
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

async def setup(bot):
    await bot.add_cog(Events(bot))