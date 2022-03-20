import os, sys
import discord
import traceback
import time
from discord.ext import commands
from discord import utils
import asyncio

try:
    with open("token.txt") as f:
        BOT_TOKEN = f.read()
except FileNotFoundError:
    print("File token.txt not found!\nCreate token.txt and place your bot token.")
    exit(1)

if len(BOT_TOKEN) < 59:
    print("Bad token, please change your token in token.txt")
    exit(1)

PREFIX="!"

class Bot(commands.Bot):
    def __init__(self):
        self._extensions = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
        intents = discord.Intents.all()
        super(Bot, self).__init__(command_prefix=PREFIX, intents=intents)

    
    def load_extensions(self):
        i = 0
        Time = time.time()
        for extension in self._extensions:
            i +=1
            try: 
                self.load_extension(f'cogs.{extension}')
                print(f'[+] Модуль {extension} загружен')
            except Exception as err: 
                exc = f'{type(err).__name__}: {err}'
                print(f'[-] Произошла ошибка при загрузке {extension}')
                traceback.print_exc()
        print(f'[{i}] модулей загружено за {round(time.time()-Time, 3)}s')

if __name__ == '__main__':
    bot = Bot()
    
    @bot.event
    async def on_ready():
        print("%s is ready" % bot.user.name)

    @bot.event
    async def on_message(message):
        if not isinstance(message.channel, discord.channel.DMChannel):
            await bot.process_commands(message)
    
    #bot.remove_command('help')

    bot.load_extensions()
    bot.run(BOT_TOKEN)
