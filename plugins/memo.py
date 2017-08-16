from plugin_base import *

from collections import defaultdict
import arrow
import os
import yaml

class MemoPlugin(Plugin):

    path = "memos.yaml"

    def __init__(self):
        super().__init__()
        self.memos = {}
        if os.path.isfile(self.path):
            with open(self.path) as datafile:
                self.memos = yaml.load(datafile)

    def save(self):
        with open(self.path, "w") as datafile:
            yaml.dump(self.memos, datafile, default_flow_style=False, allow_unicode=True)

    @command
    def tell(self, bot, event):
        """tell <user> <message> => Saves a message for user. Prints it when he says something."""
        text = event.text.strip()
        if " " not in text:
            bot.message("No message given.")
            return
        target, message = text.split(maxsplit=1)
        target, message = target.strip().rstrip(".,:"), message.strip()[:400]
        self.memos.setdefault(target, []).append(
            (event.source.nick, arrow.now(bot.timezone), message)
        )
        self.save()
        bot.message("Consider it noted.")

    @on_pubmsg
    def on_message(self, bot, event):
        nick = event.source.nick
        if nick in self.memos:
            for source, time, message in self.memos[nick][-4:]:
                time = time.format("HH:mm")
                bot.message("{}: {} | {} | {}".format(nick, source, time, message))
            del self.memos[nick]
            self.save()