import operator
import re
from functools import reduce

"""
--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two microchips, and once it does, it gives
each one to a different bot or puts it in a marked "output" bin. Sometimes, bots take microchips from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a single number; the bots must use some logic to
decide what to do with each chip. You access the local control computer and download the bots' instructions (your puzzle
input).

Some of the instructions specify that a specific-valued microchip should be given to a specific bot; the rest of the
instructions indicate what a given bot should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.

In the end, output bin 0 contains a value-5 microchip, output bin 1 contains a value-2 microchip, and output bin 2
contains a value-3 microchip. In this configuration, bot number 2 is responsible for comparing value-5 microchips with
value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible for comparing value-61 microchips with
value-17 microchips?

Your puzzle answer was 98.

--- Part Two ---

What do you get if you multiply together the values of one chip in each of outputs 0, 1, and 2?

Your puzzle answer was 4042.
"""

_bot_definition = r"value (\d+) goes to bot (\d+)"


def parse_simulation(steps):
    bots = {}

    for step in filter(lambda s: re.match(_bot_definition, s), steps):
        _parse_bot(step, bots)

    for step in filter(lambda s: re.match(r"bot \d+ gives .*", s), steps):
        _parse_rules(step, bots)

    return Simulation(bots)


def _parse_bot(step, bots):
    definition = re.match(_bot_definition, step)
    value, bot = definition.group(1), definition.group(2)
    value, bot = int(value), int(bot)
    bot = bots[bot] if bot in bots else Bot(bot)
    bot.add(value)
    bots[bot.index] = bot


def _parse_rules(step, bots):
    rule_match = re.match(r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)", step)
    bot_index = int(rule_match.group(1))
    low_destination, low_destination_index = rule_match.group(2), int(rule_match.group(3))
    high_destination, high_destination_index = rule_match.group(4), int(rule_match.group(5))

    bot = bots[bot_index] if bot_index in bots else Bot(bot_index)
    bots[bot_index] = bot

    bot.low_rule = Rule(low_destination, low_destination_index)
    bot.high_rule = Rule(high_destination, high_destination_index)


class Rule:
    def __init__(self, destination, index):
        self.destination = destination
        self.index = index

    def __call__(self, *args, **kwargs):
        simulation, value = args[0], args[1]
        simulation[self.destination](self.index).add(value)


class Bot:
    def __init__(self, index):
        self.index = index
        self.chips = set()
        self.low_rule = None
        self.high_rule = None

    def add(self, value):
        self.chips.add(value)

    def is_actionable(self):
        return len(self.chips) > 1

    def apply(self, simulation):
        low_value = min(self.chips)
        high_value = max(self.chips)

        self.low_rule(simulation, low_value)
        self.high_rule(simulation, high_value)

        self.chips = set()

        return {low_value, high_value}


class Simulation:
    def __init__(self, bots):
        self._bots = bots
        self._outputs = {}

    def bot(self, index):
        if index not in self._bots:
            self._bots[index] = Bot(index)
        return self._bots[index]

    def output(self, index):
        if index not in self._outputs:
            self._outputs[index] = set()
        return self._outputs[index]

    def step(self, stop_condition=None):
        actionable_bots = sorted(
            filter(Bot.is_actionable, self._bots.values()),
            key=lambda bot: bot.index)

        if not actionable_bots:
            raise StopIteration("No more bots to act on")

        for bot in actionable_bots:
            chips = bot.apply(self)
            if stop_condition and stop_condition(chips):
                return bot.index

    def run(self, stop_condition=None):
        while True:
            bot_index = self.step(stop_condition=stop_condition)
            if bot_index is not None:
                return bot_index

    def run_for_product_of_outputs(self, indexes):
        try:
            self.run()
        except StopIteration:
            values = list(map(self.output, indexes))

            for val in values:
                assert len(val) == 1

            return reduce(
                operator.mul,
                map(lambda val: next(iter(val)), values))

    def __getitem__(self, item):
        if item == "bot":
            return self.bot
        elif item == "output":
            return self.output


if __name__ == "__main__":
    with open("_10_bots.txt") as file:
        steps = list(map(lambda line: line.strip(), file.readlines()))
        simulation = parse_simulation(steps)
        bot = simulation.run(lambda chips: chips == {17, 61})
        print(f"p1 = {bot}")

        simulation = parse_simulation(steps)
        product = simulation.run_for_product_of_outputs([0, 1, 2])
        print(f"p2 = {product}")
