from discord.ext import commands
import discord
from EZPaginator import Paginator
import praw
from praw import models

class Subreddit(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def subreddit(self, ctx, *, name: str):
        name = name.lower().replace('r/', '')
        await ctx.trigger_typing()
        sub = self.bot.reddit.subreddit(name)
        embeds = []
        for submission in sub.new(limit=6):
            embed = discord.Embed(title=submission.title, description=submission.selftext, color=discord.Color.green(), url=f"http://reddit.com{submission.permalink}")
            embed.set_author(name=submission.author.name, icon_url=submission.author.icon_img)
            if not submission.selftext:
                embed.set_image(url=submission.url)
            embeds.append(embed)
        for i, embed in enumerate(embeds):
            embed.set_footer(text=f"page {i + 1} of {len(embeds)}")
        msg = await ctx.send(embed=embeds[0])
        pages = Paginator(self.bot, msg, embeds=embeds, timeout=60, use_more=True, only=ctx.author)
        await pages.start()

        
    @commands.command()
    async def search(self, ctx, term: str):
        await ctx.trigger_typing()
        term = term.lower().replace('r/', '')
        subs = models.Subreddits(self.bot.reddit, None).search_by_name(query=term)
        string = "\n\n".join([f"[r/{z.display_name}](https://reddit.com/r/{z.display_name}) {':underage:' if z.over18 else ''}" for z in subs])
        await ctx.send(embed=discord.Embed(title=f"search results for {term}", description=string, color=discord.Color.green()))
        


def setup(bot):
    bot.add_cog(Subreddit(bot))