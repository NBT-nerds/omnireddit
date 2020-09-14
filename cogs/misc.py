from discord.ext import commands
import discord
from utils.util import Embed


class Misc(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, *, suggestion: str):
        embed = Embed(ctx, description=suggestion).author().random_footer()
        msg = await self.bot.get_guild(self.bot.config["support_guild"]["id"]).get_channel(self.bot.config["support_guild"]["suggestion_channel"]).send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")
        await ctx.send(f'"{ctx.author.mention}Suggestion logged!")


def setup(bot):
    bot.add_cog(Misc(bot))