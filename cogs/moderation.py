import discord
from discord.ext import commands
from discord import utils


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Pings to someone."""
        await ctx.send(f'{ctx.author.mention} :ping_pong:')
    
    @commands.has_permissions(kick_members=True)
    @commands.command(name='kick', aliases=['пнуть'])
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks an user."""
        await member.kick(reason=reason)

    @commands.has_permissions(ban_members=True)
    @commands.command(name='ban', aliases=['бан'])
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans an user."""
        await member.ban(reason=reason)
    

def setup(bot):
    bot.add_cog(Moderation(bot))