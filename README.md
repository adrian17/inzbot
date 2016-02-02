### Running

Copy `example_config.yaml` to `config.yaml` and customize it to your needs.

Then:

    ./inzbot.py

### Dependencies

See requirements.txt.

Core:

- [irc](https://github.com/jaraco/irc) (My bot is basically a high-level wrapper over their low-level wrapper)
- [yaml](https://pypi.python.org/pypi/PyYAML) (for config files)

Remaining dependencies are used by the bot's plugins.

### Writing a basic plugin

```python    
from plugin_base import Plugin, command

class MyPlugin(Plugin):
    """docstring used by !help MyPlugin"""

    # reacts to !echo abc or bot_name: echo abc
    @command # optional arguments give alternative command names
    def echo(self, bot, event):
        """docstring shown by !help echo"""
        
        # event is the irc.Event object with
        # extra `text` attribute on command events
        # and `message` attribute on pubmsg events
        
        # you can also access the irc.ServerConnection object
        # with bot.connection
        # it provides wrappers for all actions like kick, mode, privmsg etc.

        # bot.message is a special utility that responds to wherever the original message was sent from
        bot.message(event.text)
    
    # triggers on every message
    @on_pubmsg
    def echo_when_duck(self, bot, event):
        if "duck" in event.message:
            bot.message('did someone say "duck"?', target=bot.channel) # forcing a message target
```