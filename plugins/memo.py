from plugin_base import *

from collections import defaultdict
import arrow

class MemoPlugin(Plugin):

    path = "memos.yaml"

    def __init__(self):
        super().__init__()
        self.state = PersistentState("memos.yaml")
        self.memos = self.state.load(default={})

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
        self.state.save(self.memos)
        bot.message("Consider it noted.")

    @on_pubmsg
    def on_message(self, bot, event):
        nick = event.source.nick
        if nick in self.memos:
            for source, time, message in self.memos[nick][-4:]:
                time = time.format("HH:mm")
                bot.message("{}: {} | {} | {}".format(nick, source, time, message))
            del self.memos[nick]
            self.state.save(self.memos)