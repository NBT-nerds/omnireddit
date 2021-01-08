from discord.ext import commands
import discord
from utils.util import Embed


class Misc(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="suggest",
                      description="log a suggestion for the bot. Join the support server to see its popularity!",
                      aliases=["suggestion"], usage="<suggestion>")
    @commands.cooldown(1,30,type=commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion: str):
        embed = Embed(ctx, description=suggestion).author().random_footer()
        msg = await self.bot.get_guild(self.bot.config["support_guild"]["id"]).get_channel(
            self.bot.config["support_guild"]["suggestion_channel"]).send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")
        await ctx.send(f"{ctx.author.mention}, Suggestion logged!")

    @commands.command(name="help", description="get a list of all the commands in the bot", usage="<command>")
    @commands.cooldown(1,2,type=commands.BucketType.user)
    async def help(self, ctx, arg: str = None):
        if arg: arg = arg.replace(ctx.prefix, "")
        command_names = [z.name.lower() for z in self.bot.commands if not z.hidden]
        for command in self.bot.commands:
            if command.hidden: continue
            for alias in command.aliases:
                command_names.append(alias.lower())
        if not arg:
            embed = Embed(ctx, title="Help",
                          description=f"Use `{ctx.prefix}help <command | category>` for more info",
                          ).random_footer()
            for cogName in self.bot.cogs:
                if cogName.lower() in self.bot.hidden_cogs: continue
                cog = self.bot.get_cog(cogName)
                string = ""
                for command in cog.get_commands():
                    if not command.hidden: string += f"`{ctx.prefix}{command.name}`\n"
                embed.add_field(name=cogName, value=string, inline=False)
            return await ctx.send(embed=embed)
        elif arg.lower() in [z.lower() for z in self.bot.cogs]:
            embed = Embed(ctx, title=f"Help for {arg} category").random_footer()
            string = ""
            cogs = {z.lower(): self.bot.cogs[z] for z in self.bot.cogs}
            cog: commands.Cog = cogs[arg]
            for command in cog.get_commands():
                if not command.hidden:  string += f"`{ctx.prefix}{command.name}` - {command.description}\n"
            embed.add_field(name="Commands", value=string, inline=False)
            await ctx.send(embed=embed)
        elif arg.lower() in command_names:
            command = self.bot.get_command(arg)
            embed = Embed(ctx, title=f"Help for `{command.name}` command").random_footer()
            embed.add_field(name=command.description or "No description",
                            value=f"**Usage**: `{ctx.prefix}{command.name}{command.usage}`\n**Aliases**: {','.join(command.aliases)}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(title="Command or category not found :(",
                                               description=f"Check your spelling from `{ctx.prefix}help` and try again",
                                               color=discord.Color.red()))


def setup(bot):
    bot.add_cog(Misc(bot))
