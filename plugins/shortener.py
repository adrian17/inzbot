from plugin_base import *

import requests

class ShortenPlugin(Plugin):

    api_url = "https://www.googleapis.com/urlshortener/v1/url"

    def shorten(self, url, api_key):
        params = {"key": api_key}
        json = {"longUrl": url}

        response = requests.post(self.api_url, params=params, json=json).json()

        return response.get("id", None)

    @on_pubmsg
    @priority(90)
    @pattern(R"(?P<url>https?://[^\s]+)")
    def listen(self, bot, event):
        if len(event.message) < 110:
            return
        url = event.match.group("url")

        short = self.shorten(url, bot.google_api_key)
        if not short:
            return
        bot.message(short)
