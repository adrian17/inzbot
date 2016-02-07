from plugin_base import *

import os
import yaml

class DefinitionsPlugin(Plugin):

    path = "definitions.yaml"

    def __init__(self):
        super().__init__()
        self.definitions = {}
        if os.path.isfile(self.path):
            with open(self.path) as datafile:
                self.definitions = yaml.load(datafile)

    def save(self):
        with open(self.path, "w") as datafile:
            yaml.dump(self.definitions, datafile)

    @command
    @admin
    def define(self, bot, event):
        """!define <name> <definition> Adds a definition. It can be accessed with !<name>."""
        if " " not in event.text:
            return
        name, definition = event.text.split(maxsplit=1)
        self.definitions[name] = definition
        self.save()
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
        if name not in self.definitions:
            return
        bot.message(self.definitions[name])

