from plugin_base import *

import requests
"""
class ShortenPlugin(Plugin):

    def shorten(self, url):
        params = {"url": url}
        return requests.get("http://tinyurl.com/api-create.php", params=params).text

    @on_pubmsg
    def listen(self, bot, event):
        match = re.search("(?P<url>https?://[^\s]+)", event.message)
        if match:
            url = match.group("url")
            short = shorten(url)
            if not short:
                return
            bot.message(short)
"""