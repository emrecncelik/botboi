import asyncio
import discord
import asyncpraw
from decouple import config
from discord.ext import commands

"""
Commands:
    -whoisthis: replies with reddit username
"""

REDDIT_USERNAME = config('REDDIT_USERNAME')
REDDIT_PASSWORD = config('REDDIT_PASSWORD')
REDDIT_CLIENT_ID = config('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = config('REDDIT_CLIENT_SECRET')

class reddit(commands.Cog, name='reddit'):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(client_id=REDDIT_CLIENT_ID,
                                       client_secret=REDDIT_CLIENT_SECRET,
                                       user_agent='discord-botboi',
                                       username=REDDIT_USERNAME,
                                       password=REDDIT_PASSWORD,
                                       redirect_url='http://localhost:8080')


    @commands.command(name='whoisthis')
    async def whoisthis(self, context):
        try:
            user = await self.reddit.user.me()
            await context.message.reply(f'Yo it\'s me, {user}')
        except Exception as ex:
            await context.message.reply(f'I don\'t know who I am anymore... (check the logs btw)')
            raise ex


def setup(bot):
    bot.add_cog(reddit(bot))