from plugin_base import *

import random
import re

class DicePlugin(Plugin):

    @staticmethod
    def dice_roll(n_dice, dice_size):
        rolls = [random.randint(1, dice_size) for _ in range(n_dice)]
        return rolls, sum(rolls)

    @command
    def roll(self, bot, event):
        """!roll k<K>, !roll <N>k<K> => Rolls N K-sided dice."""
        match = re.match(r"^(?:(\d+)?[kd])?(\d+)?$", event.text)
        if not match:
            bot.message("nie rozumiem")
            return

        dice_size = int(match.group(2))
        n_dice = int(match.group(1)) if match.group(1) else 1

        if dice_size > 1000:
            bot.message("za duza kosc")
        elif dice_size <= 1:
            bot.message("za mala kosc")
        elif n_dice > 30:
            bot.message("za duzo kosci")
        elif n_dice == 0:
            bot.message("taa, rzucaj sobie wyimaginowanymi kostkami")
        else:
            rolls, sum_dice = self.dice_roll(n_dice, dice_size)
            rolls_str = ", ".join(map(str, rolls))
            bot.message("==== {} ---> {} ====".format(rolls_str, sum_dice))