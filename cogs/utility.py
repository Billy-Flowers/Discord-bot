import discord
from discord.ext import commands

class Utility(commands.Cog):
    """Utility commands for server management"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help="Clear messages from the channel")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Clears a specified number of messages from the channel."""
        if amount <= 0:
            await ctx.send("Please provide a positive number of messages to delete.")
            return
        
        if amount > 100:
            await ctx.send("You can only delete up to 100 messages at once.")
            return
            
        await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
        await ctx.send(f"{amount} messages cleared!", delete_after=10)
    
    @commands.command(help="Get information about a user")
    async def userinfo(self, ctx, member: discord.Member = None):
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
    
    @commands.command(help="Get server information")
    async def serverinfo(self, ctx):
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
    
    @commands.command(help="Make the bot say something")
    async def say(self, ctx, *, message):
        """Makes the bot say a message."""
        await ctx.message.delete()
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Utility(bot))