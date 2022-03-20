import discord
from os import listdir
from random import randint, choice
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command()
    async def iq(self, ctx):
        iq = randint(0, 150)
        if 70 <= iq < 100:
            emoji = ":upside_down:"
        elif 50 <= iq < 70:
            emoji = ":clown:"
        elif iq >= 100:
            emoji = ":sunglasses:"
        elif iq < 50:
            emoji = ":woozy_face:"
        await ctx.send(f'{ctx.author.mention} Твой iq: **{iq}** {emoji}')
    
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command(aliases=['гей'])
    async def gay(self, ctx):
        gaypr = randint(0, 100)
        await ctx.send(f'{ctx.author.mention} Ты гей на **{gaypr}%**')
    
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command(aliases=['анимешник'])
    async def animeshnik(self, ctx):
        abobus = randint(0, 100)
        await ctx.send(f'{ctx.author.mention} Ты анимешник на **{abobus}%**')
    
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command(aliases=['dead-inside'])
    async def deadinside(self, ctx):
        dead = randint(0, 100)
        if dead >= 90:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947825252321353748/1.png')
        elif dead >= 80:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947825288266530856/20.png')
        elif dead >= 70:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947825611102093322/18.png')
        elif dead >= 60:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947825821379330078/3.png')
        elif dead >= 50:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947825897866686464/41.png')
        elif dead >= 40:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947825897866686464/41.png')
        elif dead >= 30:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947826022781427752/50.png')
        elif dead >= 20:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947826250880258058/16.png')
        elif dead >= 10:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947826354857058314/30.png')
        elif dead >= 0:
            await ctx.send('https://cdn.discordapp.com/attachments/582550611678068746/947826393062977606/52.png')
        await ctx.send(f'{ctx.author.mention} Ты дед инсайд на **{dead}%**')

def setup(bot) -> None:
    """Load the Slowmode cog."""
    bot.add_cog(Fun(bot))