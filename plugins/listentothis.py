from plugin_base import *

import requests
import random
import re

class MusicPlugin(Plugin):

    @command
    def music(self, bot, event):
        headers = {'User-Agent': bot.user_agent}
        subreddit = requests.get("https://www.reddit.com/r/listentothis.json", headers=headers).json()

        posts = subreddit["data"]["children"]
        posts = (post["data"] for post in posts)

        pattern = R".+\[.+\].+\d{4}.*" # title [genre] (year) stuff

        urls = [
            (post["url"], post["title"])
            for post in posts
            if re.match(pattern, post["title"]) is not None
        ]
        url, title = random.choice(urls)

        bot.message(url)