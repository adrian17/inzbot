from plugin_base import *

import requests
import html

class ChuckPlugin(Plugin):

    @command("chuck", "norris")
    def chuck(self, bot, event):
        """chuck => Fetches a Chuck Norris joke."""
        try:
            url = "http://api.icndb.com/jokes/random"
            json = requests.get(url).json()
            joke = json["value"]["joke"]
            joke = html.unescape(joke)
            bot.message(joke)
        except:
            logging.exception("")