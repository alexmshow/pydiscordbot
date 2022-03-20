import discord
import wikipedia
from discord.ext import commands

class Wikipedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='change_lang_wiki', hidden=True)
    async def change_lang_wiki(self, ctx, langcode: str):
        """Change wiki language."""
        wikipedia.set_lang(langcode[:2])
    
    @commands.command(name='wiki', aliases=['wikipedia'])
    async def wiki(self, ctx, *query: str):
        """Searches info about X in wikipedia."""
        wikipedia.set_lang(Options.WIKI_LANG)

        def check(message):
            return message.content.isdigit()

        try:
            text = wikipedia.summary(query, sentences=5, auto_suggest=False)
        except wikipedia.DisambiguationError as e:
            txt = ""
            for i in range(len(e.options)):
                txt += f"[**{i + 1}**] {e.options[i]}\n"
            await ctx.send("**Выберете что-то одно**:\n" + txt)
            msg = await self.bot.wait_for("message", check=check, timeout=60.0)
            try:
                try:
                    text = wikipedia.summary(e.options[int(msg.content)-1], sentences=Options.WIKI_SENTENCES, auto_suggest=False)
                    return await ctx.send(text)
                except Exception: pass
            except wikipedia.PageError:
                return await ctx.send("Ошибка такой страницы не существует.")
        except Exception as e:
            return
        await ctx.send(text)
    

def setup(bot):
    bot.add_cog(Wikipedia(bot))