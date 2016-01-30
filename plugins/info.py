from plugin_base import *

def command_name_list(plugin):
    commands = []
    for handler in plugin.command_handlers:
        commands.extend(handler.commands)
    return commands

class InfoPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.IP = None

    @command
    def commands(self, bot, event):
        func_names = []
        for plugin, handler in bot.command_handlers:
            func_names.extend(handler.commands)
        output = ", ".join(func_names)
        bot.message(output)

    @command
    def plugins(self, bot, event):
        names = []
        for plugin in bot.plugins:
            plugin_info = plugin.__class__.__name__
            func_names = command_name_list(plugin)
            if func_names:
                plugin_info += " (%s)" % ", ".join(func_names)
            names.append(plugin_info)
        names = ", ".join(names)
        bot.message(names)

    @command
    def ip(self, bot, event):
        ip = bot.connection.socket.getsockname()[0]
        bot.message(ip)

    @command
    def help(self, bot, event):
        bot.message("!help [command name|plugin name] -> shows help. Not implemented yet.")