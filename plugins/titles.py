from plugin_base import *

import logging
logging.basicConfig(format='\n%(asctime)s %(message)s', filename='../inzbot.log')

from bs4 import BeautifulSoup
import requests

def color(message):
    return "\x033" + message + "\x03"

class TitlePlugin(Plugin):

    @on_pubmsg
    @priority(70)
    def handle_line(self, bot, event):
        header = {'User-Agent': bot.user_agent}

        message = event.message
        if message.startswith("http:") or message.startswith("https:"):
            try:
                response = requests.get(message, headers=header)
                if 'text/html' in response.headers['content-type']:
                    soup = BeautifulSoup(response.text, "html.parser")
                    title = soup.find("title").text.strip()
                    message = color("==== ") + title + color(" ====")
                    bot.message(message)
                    return True
            except Exception:
                logging.exception("")