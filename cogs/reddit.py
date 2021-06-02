import asyncpraw
from decouple import config
from discord.ext import commands

"""
Commands:
    -whoisthis: replies with reddit username
    -sub: lists n number submissions from a given subreddit and time filter
    -subsearch: lists n number of submissions from a given subreddit and time
        filter with search query

TODO
-Add support for multiple word search query and command options
    -ex. !command -opt1 input1 -opt2 input2
    -maybe merge !subsearch with !sub?
-Find a better way to initialize and close reddit instance (client)
"""

REDDIT_USERNAME = config('REDDIT_USERNAME')
REDDIT_PASSWORD = config('REDDIT_PASSWORD')
REDDIT_CLIENT_ID = config('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = config('REDDIT_CLIENT_SECRET')


class reddit(commands.Cog, name='reddit'):
    def __init__(self, bot):
        self.bot = bot

    def init_reddit_client(self):
        self.reddit = asyncpraw.Reddit(client_id=REDDIT_CLIENT_ID,
                                       client_secret=REDDIT_CLIENT_SECRET,
                                       user_agent='discord-botboi',
                                       username=REDDIT_USERNAME,
                                       password=REDDIT_PASSWORD,
                                       redirect_url='http://localhost:8080')

    @commands.command(name='whoisthis')
    async def whoisthis(self, context):
        self.init_reddit_client()
        try:
            user = await self.reddit.user.me()
            await context.message.reply(f'Yo it\'s me, {user}')
        except Exception as ex:
            await context.message.reply(
                'I don\'t know who I am anymore... (check the logs btw)')
            raise ex
        finally:
            await self.reddit.close()

    @commands.command(name='sub')
    async def sub(self,
                  context,
                  subreddit_name: str,
                  time_filter: str = 'all',
                  num_of_submissions: int = 5):
        # max of 10 posts allowed at once
        try:
            if num_of_submissions > 10:
                num_of_submissions = 10
            self.init_reddit_client()
            subreddit = await self.reddit.subreddit(
                display_name=subreddit_name)

            # allowed time filters: day, week, hour, month, all, year
            async for submission in subreddit.top(time_filter=time_filter,
                                                  limit=num_of_submissions):
                await context.channel.send(submission.url)
        finally:
            await self.reddit.close()

    @commands.command(name='subsearch')
    async def subsearch(self,
                        context,
                        subreddit_name: str,
                        query: str,
                        time_filter: str = 'all',
                        num_of_submissions: int = 5,
                        sort: str = 'top'):
        try:
            self.init_reddit_client()
            subreddit = await self.reddit.subreddit(
                display_name=subreddit_name)
            async for submission in subreddit.search(query=query,
                                                     sort=sort,
                                                     time_filter=time_filter,
                                                     limit=num_of_submissions):
                await context.channel.send(submission.url)
        finally:
            await self.reddit.close()


def setup(bot):
    bot.add_cog(reddit(bot))
