from discord.ext import commands
import discord
from utils.util import Embed


class Misc(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="suggest", description="log a suggestion for the bot. Join the support server to see its popularity!", aliases=["suggestion"], usage="<suggestion>")
    async def suggest(self, ctx, *, suggestion: str):
        embed = Embed(ctx, description=suggestion).author().random_footer()
        msg = await self.bot.get_guild(self.bot.config["support_guild"]["id"]).get_channel(self.bot.config["support_guild"]["suggestion_channel"]).send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")
        await ctx.send(f"{ctx.author.mention}, Suggestion logged!")

    @commands.command(name="help",description="get a list of all the commands in the bot",usage="<command>")
    async def help(self,ctx):
        embed = discord.Embed(color=0x0080ff).set_author
        (name=ctx.author,icon_url=ctx.author.avatar_url).add_field
        (name="Admin Commands",value="reload,reload_config",inline=False).add_field
        (name="Reddit Commands",value="searchpost,searchsubreddit,subreddit,user")
        (name="Misc",value="help,prefix,suggest")
        await ctx.send(embed=embed)
    
    @commands.command(name="prefix",description="changes/checks prefix of bot",usage="<prefix>")
    async def prefix(self, ctx,*, prefix):
        pass

def setup(bot):
    bot.add_cog(Misc(bot))