from plugin_base import *

import logging

from bs4 import BeautifulSoup
import requests

def color(message):
    return "\x033" + message + "\x03 "

class TitlePlugin(Plugin):
    """Prints titles of web pages."""

    @on_pubmsg
    @priority(70)
    @pattern(R"(?P<url>https?://[^\s]+)")
    def handle_line(self, bot, event):
        header = {
            'User-Agent': bot.user_agent,
            'Accept-Language': 'en'
        }

        url = event.match.group("url")

        try:
            response = requests.get(url, headers=header, timeout=5, stream=True)
            if 'text/html' in response.headers['content-type']:
                # hack :/ Let's assume that most sites actually serve UTF-8 (FB does, for example)
                if response.encoding == 'ISO-8859-1':
                    response.encoding = 'UTF-8'
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.find("title").text.strip()
                message = color("↳ ") + title
                bot.message(message)
                return True
        except requests.exceptions.Timeout:
            bot.message("{}: timeout after 5s.".format(url))
        except Exception:
            logging.exception("")