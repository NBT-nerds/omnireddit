import discord
from discord.ext import commands
import praw
from datetime import datetime
from utils.paginator import Paginator
from utils import redditutils

class RedditMisc(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name="user", description="Get some info about a specific redditor", aliases=["redditor"], usage="<username>")
    async def user(self, ctx: commands.Context, *, name: str):
        redditor = self.bot.reddit.redditor(name.lower().replace('u/', ''))
        embed = discord.Embed(description="**Created at: **{}".format(datetime.fromtimestamp(redditor.created_utc).strftime("%d/%m/%Y, %H:%M:%S")), color=(discord.Color.gold() if redditor.is_gold else discord.Color.darker_grey())).set_author(name=redditor.name, icon_url=redditor.icon_img)
        embed.add_field(name=f"Karma: {redditor.comment_karma + redditor.link_karma}", value=f"Comment Karma: {redditor.comment_karma}\nLink Karma: {redditor.link_karma}")
        await ctx.send(embed=embed)

    @commands.command()
    async def test(self, ctx):
        await ctx.send("⇧")

    @commands.command(name="searchPost", description="Search for a post.", usage="<keyword>")
    async def searchPost(self, ctx, *, query:str):
        await ctx.trigger_typing()
        sub = self.bot.reddit.subreddit("all")
        embeds = []
        for i, submission in enumerate(sub.search(query)):
            if i > 4:
                break
            if submission.over_18 and not ctx.channel.is_nsfw():
                raise commands.NSFWChannelRequired(ctx.channel)
            if embed := redditutils.format_submission_embed(submission):
                embeds.append(embed)
        if not embeds:
            return await ctx.send(embed=discord.Embed(title="no results :(", color=discord.Color.red()))
        msg = await ctx.send(embed=embeds[0])
        pages = Paginator(self.bot, msg, embeds=embeds, timeout=60, use_more=True, only=ctx.author).set_page_footers()
        await pages.start()


def setup(bot):
    bot.add_cog(RedditMisc(bot))