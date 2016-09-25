from functools import wraps
import inspect

class Plugin:
    def __init__(self):

        self.command_handlers = []
        self.pubmsg_handlers = []

        handlers = [
            handler
            for name, handler
            in inspect.getmembers(self.__class__, predicate=inspect.isfunction)
        ]
        for handler in handlers:
            if not hasattr(handler, "on_pubmsg"):
                handler.on_pubmsg = False
            if not hasattr(handler, "patterns"):
                handler.patterns = []
            if not hasattr(handler, "commands"):
                handler.commands = []
            if not hasattr(handler, "priority"):
                handler.priority = 50
            if not hasattr(handler, "admin_only"):
                handler.admin_only = False

            if handler.commands:
                self.command_handlers.append(handler)
            if handler.on_pubmsg:
                self.pubmsg_handlers.append(handler)

def priority(value):
    def decorator(function):
        function.priority = value
        return function
    return decorator

def command(*commands):
    def add_commands(function, commands):
        if not hasattr(function, "commands"):
            function.commands = []
        function.commands.extend(commands)
        return function

    if callable(commands[0]):
        function = commands[0]
        return add_commands(function, [function.__name__])
    def decorator(function):
        return add_commands(function, commands)
    return decorator

def on_pubmsg(function):
    function.on_pubmsg = True
    return function

def pattern(pattern_str):
    def decorator(function):
        if not hasattr(function, "patterns"):
            function.patterns = []
        function.patterns.append(pattern_str)
        return function
    return decorator

def admin(function):
    function.admin_only = True
    @wraps(function)
    def admin_function(self, bot, event):
        if event.source.nick in bot.admins:
            function(self, bot, event)
    return admin_function