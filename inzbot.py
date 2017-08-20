#! /usr/bin/env python3

import logging

from pathlib import Path
import re
import textwrap
import sys

import irc.bot
import irc.strings
irc.client.ServerConnection.buffer_class.errors = 'replace'
import yaml

from plugin_base import Plugin
from plugins import *

class InzBot(irc.bot.SingleServerIRCBot):
    def __init__(self):
        logging.info("Loading config")
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
        self.google_api_key = config["other"]["google-api-key"]
        self.google_search_engine = config["other"]["google-search-engine"]
        self.nsjail_path = config['other']['nsjail_path']
        if self.nsjail_path is None and Path('/bin/nsjail').exists():
            self.nsjail_path = '/bin/nsjail'

        self.admins = config["admins"]
        self.blacklist = config["blacklist"]
        self.disabled_commands = config["disabled_commands"]

        self.plugins = []
        self.command_handlers = []
        self.pubmsg_handlers = []

        num_plugins = len(Plugin.__subclasses__())
        logging.info("Found {} plugins".format(num_plugins))

        for PluginClass in Plugin.__subclasses__():
            logging.info("Loading {}".format(PluginClass.__name__))

            plugin = PluginClass()
            self.command_handlers.extend([(plugin, handler) for handler in plugin.command_handlers])
            self.pubmsg_handlers.extend([(plugin, handler) for handler in plugin.pubmsg_handlers])
            self.plugins.append(plugin)
        self.command_handlers.sort(key=lambda kv: kv[1].priority, reverse=True)
        self.pubmsg_handlers.sort(key=lambda kv: kv[1].priority, reverse=True)

        logging.info("Initialized")

    def on_nicknameinuse(self, c, e):
        nick = c.get_nickname()
        new_nick = nick + "_"
        logging.info("Nickname {} in use, changing to {}".format(nick, new_nick))
        c.nick(new_nick)

    def on_welcome(self, c, e):
        logging.info("Connected to the network")
        if self.nickpass:
            c.privmsg('NickServ', 'identify {}'.format(self.nickpass))

        logging.info("Joining the channel")
        c.join(self.channel)

    def message(self, message, target=None, wrap=False):
        if target == None:
            target = self.target
        message = message.rstrip().replace("\n", "").replace("\r", "")

        if wrap:
            messages = textwrap.wrap(message, width=256)
        else:
            messages = [message]

        for message in messages:
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
            executed = self.do_command(e, command.strip(), allow_passthrough=True)
            if executed:
                return

        for plugin, handler in self.pubmsg_handlers:
            if handler.patterns:
                for pattern in handler.patterns:
                    match = re.search(pattern, message)
                    if match:
                        e.match = match
                        break
                else:
                    continue
            e.message = message
            success = handler(plugin, self, e)
            if success:
                return

    def do_command(self, e, cmd, priv=False, allow_passthrough=True):
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
            return True
        if not allow_passthrough:
            self.message("Zla komenda: " + command)
            return True
        else:
            return False

def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(module)s - %(message)s', level=logging.INFO)
    bot = InzBot()
    try:
        bot.start()
    except:
        logging.exception("")
        logging.info("Closing due to error")
        sys.exit(1)
    logging.info("Closing")

if __name__ == "__main__":
    main()
