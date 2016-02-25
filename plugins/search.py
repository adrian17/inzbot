from plugin_base import *

import logging
logging.basicConfig(format='\n%(asctime)s %(message)s', filename='../inzbot.log')

import requests

def do_google_request(bot, query):
    api = "https://www.googleapis.com/customsearch/v1?parameters"
    params = {"key": bot.google_api_key, "cx": bot.google_search_engine, "q": query}
    header = {'User-Agent': bot.user_agent}

    try:
        response = requests.get(api, params=params, headers=header).json()
        return response["items"][0]["link"]
    except Exception:
        logging.exception("")
        return None

class SearchPlugin(Plugin):
    @command
    def google(self, bot, event):
        """!google <query> => Makes a google search and returns first result."""
        if not event.text:
            return
        url = do_google_request(bot, event.text)
        if url:
            bot.message(url)

    @command
    def xkcd(self, bot, event):
        """!xkcd <query> => Returns the best found xkcd strip."""
        if not event.text:
            return
        query = "site:xkcd.com -site:*.xkcd.com " + event.text
        url = do_google_request(bot, query)
        if url:
            bot.message(url)