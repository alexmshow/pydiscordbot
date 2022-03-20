import re
import discord

from discord.ext.commands import Cog

array = []
with open("blacklist.txt", "r") as file:
    fileread = file.read()
    array = fileread.split("\n")


class Message:
    def __init__(self, message):
        self.message = message

    @property
    def is_dm(self):
        return True if isinstance(self.message.channel, discord.channel.DMChannel) else False
    
    def check_for_bad_message(self):
        for i in range(len(array)):
            if re.search(array[i], self.message.content):
                return True
        return False


class Anti_spam(Cog):
    """Filter"""
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_message(self, message):
        mes = Message(message)
        if not mes.is_dm:
            if mes.check_for_bad_message():
                await message.delete()
                await message.author.ban(reason="реклама", delete_message_days=2)
    
    @Cog.listener()
    async def on_message_edit(self, before, message):
        mes = Message(message)
        if not mes.is_dm:
            if mes.check_for_bad_message():
                await message.delete()
                await message.author.ban(reason="реклама", delete_message_days=2)


def setup(bot) -> None:
    """Load the Slowmode cog."""
    bot.add_cog(Anti_spam(bot))