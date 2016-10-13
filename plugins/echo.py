from plugin_base import *

from unidecode import unidecode
import subprocess

def make_action(message):
    return "\x01ACTION " + message + "\x01"

class EchoPlugin(Plugin):

    @command
    @admin
    def echo(self, bot, event):
        """echo <message> => Prints a message to channel."""
        bot.message(event.text, target=bot.channel)

    @command
    @admin
    def echo_to(self, bot, event):
        """echo <target message> => Prints a message to a target."""
        if " " not in event.text:
            return
        target, message = event.text.split(maxsplit=1)
        bot.message(message, target=target)

    @command
    @admin
    def action_echo(self, bot, event):
        """action_echo <message> => Prints a message to channel with /me."""
        bot.message(make_action(event.text), target=bot.channel)

    @command
    def next(self, bot, event):
        bot.message("Another satisfied customer, next!")

    @on_pubmsg
    @priority(10)
    @pattern("naleśnik")
    def handle_line(self, bot, event):
        bot.message("(smacznego)")

    @command
    def figlet(self, bot, event):
        """figlet <text> => Prints a result of the "figlet" program."""
        text = unidecode(event.text.strip())
        output = subprocess.check_output(['figlet', text]).decode('utf-8').splitlines()[:6]
        for line in output:
            line = line.rstrip()
            if not line:
                continue
            bot.message(line)

    @command
    def flip(self, bot, event):
        """flip [<message>] => Flips table or a message."""
        if not event.text:
            bot.message("(╯°□°）╯︵ ┻━┻", target=bot.channel)
        else:
            normal   = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890.,!?）)(_><"
            upsidedown = "∀ᗺƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄ZɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎzƖᄅƐㄣϛ9ㄥ860˙'¡¿(()¯<>"
            mapping = {a: b for a, b in zip(normal, upsidedown)}
            flipped = "".join(mapping.get(c, c) for c in reversed(event.text))
            bot.message("(╯°□°）╯︵ " + flipped, target=bot.channel)

    @command
    def slap(self, bot, event):
        """slap <username>|all => Slap a user or all users."""
        target, *rest = event.text.strip().split(maxsplit=1)
        rest = rest[0] if rest else "with a pancake"
        users = list(bot.channels[bot.channel].users())
        if target == "all":
            for user in users:
                bot.message(make_action("slaps " + user + " " + rest), target=bot.channel)
        elif target in users:
            bot.message(make_action("slaps " + target + " " + rest), target=bot.channel)
        else:
            bot.message(make_action("can't find " + target), target=bot.channel)
