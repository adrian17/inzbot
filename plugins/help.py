from plugin_base import *

def find_command_by_name(bot, name):
	for _, handler in bot.command_handlers:
		if name in handler.commands:
			return handler

def find_plugin_by_name(bot, name):
	for plugin in bot.plugins:
		if name == plugin.__class__.__name__:
			return plugin

class HelpPlugin(Plugin):

	@command
	def help(self, bot, event):
		"""help <command name>|<plugin name> => Shows help."""

		name = event.text

		if not name:
			bot.message(self.help.__doc__)
			return
		command = find_command_by_name(bot, name)
		if command:
			if command.__doc__:
				doc = command.__doc__
				if command.admin_only:
					doc = "(admin command) " + doc
				bot.message(doc)
			else:
				bot.message("This command has no help text.")
			return
		plugin = find_plugin_by_name(bot, name)
		if plugin:
			if plugin.__doc__:
				bot.message(plugin.__doc__)
			else:
				bot.message("This plugin has no help text. Try checking individual commands.")
			return
		bot.message("Didn't find such command/plugin.")