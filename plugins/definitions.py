from plugin_base import *

class DefinitionsPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.definitions = {}

    @command
    @admin
    def define(self, bot, event):
        """!define <name> <definition> Adds a definition. It can be accessed with !<name>."""
        if " " not in event.text:
            return
        name, definition = event.text.split(maxsplit=1)
        self.definitions[name] = definition
        bot.message("Saved.")

    @command
    def definitions(self, bot, event):
        """Shows all saved definitions."""
        names = self.definitions.keys()
        bot.message(", ".join(names))

    @on_pubmsg
    @pattern(R"^!(?P<name>\w+)$")
    def listen(self, bot, event):
        name = event.match.group("name")
        print(name)
        print(self.definitions)
        if name not in self.definitions:
            return
        bot.message(self.definitions[name])

