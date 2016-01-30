from plugin_base import *

import subprocess

class AdminPlugin(Plugin):

    @command("opme", "su")
    @admin
    def opme(self, bot, event):
        bot.connection.mode(bot.channel, "+o " + event.source.nick)

    @command("deopme", "desu")
    @admin
    def deopme(self, bot, event):
        bot.connection.mode(bot.channel, "-o " + event.source.nick)

    @command("giveop")
    @admin
    def op(self, bot, event):
        bot.connection.mode(bot.channel, "+o " + event.text)

    @command
    @admin
    def kick(self, bot, event):
        users = list(bot.channels[bot.channel].users())
        nick = event.text
        if nick in users:
            bot.connection.kick(bot.channel, nick)
        else:
            bot.message("No such nick here")

    @command
    @admin
    def topic(self, bot, event):
        new_topic = event.text
        bot.connection.topic(bot.channel, new_topic=new_topic)

    @command
    @admin
    def reconnect(self, bot, event):
        bot.disconnect() # The bot will try to reconnect after 60 seconds.

    @command
    @admin
    def die(self, bot, event):
        bot.die()

    @command
    @admin
    def top(self, bot, event):
        command = "top -d1 -b -n2 -o \"-%CPU\" | tail -n 3 | tac | awk '{print $1, $2, $9, $10, $11, $12}'"
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        for line in output.splitlines():
            bot.message(line)

    @command
    @admin
    def prompt(self, bot, event):
        text = event.text
        if text == 'disable':
            bot.short_prompt = False
            bot.message('(disabled short prompt)')
        elif text == 'enable':
            bot.short_prompt = True
            bot.message('(enabled short prompt)')
        else:
            if not text or len(text) > 4:
                return
            elif text[0].isalnum() or text[-1].isalnum():
                return
            bot.prompt_start = text
            bot.message('(changed prompt to {})'.format(text))