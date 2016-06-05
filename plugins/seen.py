from plugin_base import *

import arrow

class LastSeenPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.seen = {}

    @command
    def seen(self, bot, event):
        """seen <user> => Tells the last time a user was active"""
        nick = event.text.strip()
        if nick not in self.seen:
            bot.message("I can't find {}".format(nick))
            return
        last_seen, last_message = self.seen[nick]

        if len(last_message) > 50:
            last_message = last_message[:50] + "[...]"

        bot.message("{} was last seen on {}, he said '{}'".format(
            nick, last_seen.format('YYYY-MM-DD HH:mm:ss'), last_message
        ))

    @on_pubmsg
    def on_message(self, bot, event):
        nick = event.source.nick
        self.seen[nick] = (arrow.now(), event.message)