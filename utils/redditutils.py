import praw.models
import discord

def isImageLink(url:str):
    return True in [True for z in [".jpg", ".webp", ".png"] if z in url]

def format_submission_embed(submission: praw.models.Submission):
    if len(submission.selftext) > 2048 or len(submission.title) > 256:
        return None
    embed = discord.Embed(title=submission.title, description=f"{submission.selftext}\n\n⇧      {submission.score:,}      ⇩", color=discord.Color.green(), url=f"http://reddit.com{submission.permalink}")
    embed.set_author(name=submission.author.name, icon_url=submission.author.icon_img)
    if not submission.selftext:
        if not isImageLink(submission.url):
            return None
        embed.set_image(url=submission.url)
    return embed
