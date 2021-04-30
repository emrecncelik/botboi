# -*- coding: utf-8 -*-
import praw
from decouple import config

class reddit_bot():

    def __init__(self):
        self.client_id = config("REDDIT_CLIENT_ID")
        self.client_secret = config("REDDIT_CLIENT_SECRET")
        self.user_agent = config("REDDIT_USER_AGENT")
        self.bot = praw.Reddit(client_id=self.client_id,client_secret=self.client_secret,user_agent=self.user_agent)

    

    def get_random_post_image_from_subreddit(self,given_subreddit):
        subreddit = self.bot.subreddit(given_subreddit)
        
        random=subreddit.random()
        print(random.url)
        
            

bot = reddit_bot()

bot.get_random_post_image_from_subreddit("gonewild")
            

        