from discord.ext import commands
import discord
import os
from utils.util import bot_staff, getConfig
from loguru import logger


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.check(bot_staff)
    @commands.command(hidden=True)
    async def reload(self, ctx: commands.Context):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    self.bot.reload_extension(f"cogs.{filename[:-3]}")
                    logger.info(f"reloaded cogs.{filename[:-3]}")
                except commands.ExtensionNotLoaded:
                    self.bot.load_extension(f"cogs.{filename[:-3]}")
                    logger.info(f"loaded cogs.{filename[:-3]}")
        logger.info("Cogs reloaded, bot ready")
        await ctx.message.add_reaction("👌")

    @commands.command(hidden=True)
    @commands.check(bot_staff)
    async def reload_config(self, ctx):
        self.bot.config = getConfig()
        return await ctx.send(f"`config reloaded by` {ctx.author.mention}")


def setup(bot):
    bot.add_cog(Admin(bot))
