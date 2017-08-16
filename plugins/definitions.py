from plugin_base import *

class DefinitionsPlugin(Plugin):

    def __init__(self):
        super().__init__()
        self.state = PersistentState("definitions.yaml")
        self.definitions = self.state.load(default={})

    @command
    @admin
    def define(self, bot, event):
        """define <name> <definition> => Adds a definition. It can be accessed with !<name>."""
        if " " not in event.text:
            return
        name, definition = event.text.split(maxsplit=1)
        name = name.lower()
        if not name[0].isalpha():
            bot.message("Name should start with a letter")
            return
        self.definitions[name] = definition
        self.state.save(self.definitions)
        bot.message("Saved.")

    @command
    def definitions(self, bot, event):
        """definitions => Shows all saved definitions."""
        names = sorted(self.definitions.keys())
        bot.message(", ".join(names), wrap=True)

    @command
    def give(self, bot, event):
        """give <user> <definition> => Sends contents of definition to a user."""
        if " " not in event.text:
            return
        nick, name = event.text.split(maxsplit=1)
        name = name.lower()
        if name not in self.definitions:
            return
        bot.message("{}: {}".format(nick, self.definitions[name]))

    @on_pubmsg
    @pattern(R"^!(?P<name>[\w-]+)$")
    def listen(self, bot, event):
        name = event.match.group("name").lower()
        if name not in self.definitions:
            return
        bot.message(self.definitions[name])

