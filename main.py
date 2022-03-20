import os, sys
import discord
import traceback
import colorama
import time
from discord.ext import commands
from discord import utils
import asyncio


with open("token.txt") as f:
    BOT_TOKEN = f.read()
PREFIX="!"

colorama.init()

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
                print(f'[+] {colorama.Fore.GREEN}Модуль {colorama.Style.RESET_ALL}{extension} {colorama.Fore.GREEN}загружен{colorama.Style.RESET_ALL}')
            except Exception as err: 
                exc = f'{type(err).__name__}: {err}'
                print(f'[-] {colorama.Fore.RED}Произошла ошибка при загрузке{colorama.Style.RESET_ALL} {extension}')
                traceback.print_exc()
        print(f'[{i}] {colorama.Fore.GREEN}модулей загружено{colorama.Style.RESET_ALL} за {round(time.time()-Time, 3)}s')

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
