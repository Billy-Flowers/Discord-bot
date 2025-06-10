import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    """Fun commands for entertainment"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="8ball", help="Ask a yes/no question")
    async def eight_ball(self, ctx, *, question):
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
    
    @commands.command(help="Ask who will do something")
    async def who(self, ctx, *, question):
        """Randomly selects a server member to answer 'who' questions."""
        members = [member.name for member in ctx.guild.members if not member.bot]
        if members:
            await ctx.send(f'Who {question}?\n{random.choice(members)}')
        else:
            await ctx.send("I couldn't find any members to choose from.")
    
    @commands.command(help="Check someone's vibe")
    async def vibecheck(self, ctx, *, subject):
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
    
    @commands.command(help="Roll a dice")
    async def roll(self, ctx, dice: str = "1d6"):
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

async def setup(bot):
    await bot.add_cog(Fun(bot))