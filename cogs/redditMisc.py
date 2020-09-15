import discord
from discord.ext import commands
import praw
from datetime import datetime

class RedditMisc(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def user(self, ctx: commands.Context, *, name: str):
        redditor = self.bot.reddit.redditor(name.lower().replace('u/', ''))
        embed = discord.Embed(description="**Created at: **{}".format(datetime.fromtimestamp(redditor.created_utc).strftime("%d/%m/%Y, %H:%M:%S")), color=(discord.Color.gold() if redditor.is_gold else discord.Color.darker_grey())).set_author(name=redditor.name, icon_url=redditor.icon_img)
        embed.add_field(name=f"Karma: {redditor.comment_karma + redditor.link_karma}", value=f"Comment Karma: {redditor.comment_karma}\nLink Karma: {redditor.link_karma}")
        await ctx.send(embed=embed)
        


def setup(bot):
    bot.add_cog(RedditMisc(bot))