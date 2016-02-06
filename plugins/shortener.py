from plugin_base import *

import re

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
    def listen(self, bot, event):
        message = event.message
        if len(message) < 110:
            return
        match = re.search(R"(?P<url>https?://[^\s]+)", event.message)
        if not match:
            return
        url = match.group("url")

        short = self.shorten(url, bot.google_api_key)
        if not short:
            return
        bot.message(short)
