#! /usr/bin/env python3

import logging
logging.basicConfig(format='\n%(asctime)s %(message)s', filename='../inzbot.log')

import irc.bot
import irc.strings
irc.client.ServerConnection.buffer_class.errors = 'replace'
import yaml

from plugin_base import Plugin
from plugins import *

class InzBot(irc.bot.SingleServerIRCBot):
    def __init__(self):
        config = yaml.load(open("config.yaml"))
        server, port, channel = config["server"], config["port"], config["channel"]
        nickname, nickpass = config["nickname"], config["nickpass"]

        super().__init__([(server, port)], nickname, nickname)
        self.channel = channel
        self.nickpass = nickpass
        self.timezone = config["timezone"]

        self.short_prompt = True if config["prompt"] else False
        self.prompt_start = config["prompt"]

        self.user_agent = config["other"]["user-agent"]
        self.youtube_api_key = config["other"]["youtube-api-key"]

        self.admins = config["admins"]
        self.blacklist = config["blacklist"]
        self.disabled_commands = config["disabled_commands"]

        self.plugins = []
        self.command_handlers = []
        self.pubmsg_handlers = []
        for PluginClass in Plugin.__subclasses__():
            plugin = PluginClass()
            self.command_handlers.extend([(plugin, handler) for handler in plugin.command_handlers])
            self.pubmsg_handlers.extend([(plugin, handler) for handler in plugin.pubmsg_handlers])
            self.plugins.append(plugin)
        self.command_handlers.sort(key=lambda kv: kv[1].priority, reverse=True)
        self.pubmsg_handlers.sort(key=lambda kv: kv[1].priority, reverse=True)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        if self.nickpass:
            c.privmsg('NickServ', 'identify {}'.format(self.nickpass))
        c.join(self.channel)

    def message(self, message, target=None):
        if target == None:
            target = self.target
        message = message.strip().replace("\n", "").replace("\r", "")
        self.connection.privmsg(target, message)

    def on_privmsg(self, c, e):
        if e.source.nick in self.blacklist:
            return
        message = e.arguments[0]
        self.target = e.source.nick
        self.connection = c
        self.do_command(e, e.arguments[0], True)

    def on_pubmsg(self, c, e):
        if e.source.nick in self.blacklist:
            return
        message = e.arguments[0]
        self.target = e.target
        self.connection = c

        if ":" in message:
            nick, command = message.split(":", 1)
            if nick.lower() == self.connection.get_nickname().lower():
                self.do_command(e, command.strip())
                return

        if self.short_prompt and message.startswith(self.prompt_start):
            command = message[len(self.prompt_start):]
            self.do_command(e, command.strip(), notify=False)
            return

        for plugin, handler in self.pubmsg_handlers:
            e.message = message
            success = handler(plugin, self, e)
            if success:
                return

    def do_command(self, e, cmd, priv=False, notify=True):
        if priv and e.source.nick != "adrian17":
            self.message(e.source.nick + " asked me to: " + cmd, target="adrian17")
        command, *arg = cmd.split(" ", 1)
        for plugin, handler in self.command_handlers:
            if command not in handler.commands:
                continue
            if command in self.disabled_commands:
                continue
            e.text = arg[0].strip() if arg else ""
            handler(plugin, self, e)
            return
        if notify:
            self.message("Zla komenda: " + command)

def main():
    bot = InzBot()
    try:
        bot.start()
    except:
        logging.exception("")

if __name__ == "__main__":
    main()
