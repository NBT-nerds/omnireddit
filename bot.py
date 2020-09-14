from discord.ext import commands
import discord
import os
from loguru import logger
import traceback
import praw

from utils.util import getConfig


class Omnireddit(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="r/")
        self.load_cogs().

        self.config = getConfig()
        self.reddit = praw.Reddit(client_id=self.config["reddit"]["client_id"],
                     client_secret=self.config["reddit"]["client_secret"],
                     user_agent=self.config["reddit"]["user_agent"])

        self.load_cogs()

    def load_cogs(self):
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"cogs.{name}")
                    logger.info(f"Loaded cogs.{name}")
                except Exception as e:
                    logger.error(f"Couldn't load: {name}.")
                    logger.exception(e)

    async def on_ready(self):
        logger.info("Cogs loaded, bot ready")

    async def on_command_error(self, ctx : commands.Context, exception):
        if isinstance(exception, commands.CommandNotFound):
            return #await ctx.send("`Command not found`", delete_after=3)
        if isinstance(exception, commands.NoPrivateMessage):
            return await ctx.send("This command can't be used in a private chat.", delete_after=7)
        if isinstance(exception, commands.CommandOnCooldown):
            return await ctx.send("This command is on cooldown, please wait " + str(round(exception.retry_after, 2)) + " more seconds!", delete_after=7)
        if isinstance(exception, commands.MissingRequiredArgument):
            await ctx.send("You are Missing required arguments!", delete_after=7)
            # return await ctx.invoke(self.get_command("help show_command"), arg=ctx.command)
        if isinstance(exception, commands.BadArgument):
            return await ctx.send(f"This is an invalid argument.\n`{exception}`")
        if isinstance(exception, commands.CheckFailure):
            return await ctx.send("It seems like you do not have permissions to run this.")
        if isinstance(exception, commands.TooManyArguments):
            return await ctx.send("You Provided too many arguments.")
        
        if isinstance(exception, commands.CommandInvokeError):
            if isinstance(exception.original, discord.Forbidden):
                try:
                    return await ctx.author.send(f"I couldn't respond in {ctx.channel.mention}, because I have no permissions to send messages there.")
                except discord.Forbidden:
                    pass
                logger.exception(exception)
                return await ctx.send("An unknown error occurred. Please report this to the devs.")
        traceback_lines = traceback.format_exception(type(exception), exception, exception.__traceback__)
        logger.exception("".join(traceback_lines))
        logger.exception(exception)


if __name__ == "__main__":
    bot = Omnireddit()
    try:
        bot.run(bot.config["token"])
    except discord.LoginFailure:
        logger.exception("Invalid token in config.json")