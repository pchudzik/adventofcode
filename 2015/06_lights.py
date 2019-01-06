"""
--- Day 6: Probably a Fire Hazard ---

Because your neighbors keep defeating you in the holiday house decorating contest year after year, you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include whether to turn on, turn off, or toggle various inclusive ranges given as coordinate pairs. Each coordinate pair represents opposite corners of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by doing the instructions Santa sent you in order.

For example:

turn on 0,0 through 999,999 would turn on (or leave on) every light.
toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning off the ones that were on, and turning on the ones that were off.
turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.
After following the instructions, how many lights are lit?

Your puzzle answer was 543903.

--- Part Two ---

You just finish implementing your winning light pattern when you realize you mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of those lights by 1.

The phrase turn off actually means that you should decrease the brightness of those lights by 1, to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of those lights by 2.

What is the total brightness of all lights combined after following Santa's instructions?

For example:

turn on 0,0 through 0,0 would increase the total brightness by 1.
toggle 0,0 through 999,999 would increase the total brightness by 2000000.
Your puzzle answer was 14687245.
"""


class Lights:

    def __init__(self, size, inital):
        self.inital = inital
        self.grid = [[inital] * size for grid_size in range(size)]

    def execute(self, command):
        actions = {
            "on": self.turn_on,
            "off": self.turn_off,
            "toggle": self.toggle
        }
        cmd = command[0]
        start = command[1]
        end = command[2]
        actions[cmd](start, end)

    def turn_on(self, start, end):
        raise NotImplementedError

    def toggle(self, start, end):
        raise NotImplementedError

    def turn_off(self, start, end):
        raise NotImplementedError

    def _action(self, start, end, action):
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                self.grid[x][y] = action(self.grid[x][y])


class SimpleLights(Lights):

    def __init__(self, size, initial):
        Lights.__init__(self, size, initial)

    @property
    def number_of_lit_lights(self):
        return [light for row in self.grid for light in row].count(True)

    def turn_on(self, start, end):
        self._action(start, end, lambda light: True)

    def toggle(self, start, end):
        self._action(start, end, lambda light: not light)

    def turn_off(self, start, end):
        self._action(start, end, lambda light: False)


class LightsWithBrightnessControll(Lights):

    def __init__(self, size, initial):
        Lights.__init__(self, size, initial)

    @property
    def total_brightness(self):
        return sum([light for row in self.grid for light in row])

    def turn_on(self, start, end):
        self._action(start, end, lambda light: light + 1)

    def toggle(self, start, end):
        self._action(start, end, lambda light: light + 2)

    def turn_off(self, start, end):
        self._action(start, end, lambda light: light - 1 if light > 0 else 0)


def parse_commands(commands):
    return map(parse_command, commands)


def parse_command(command):
    action_command = ""
    start = ()
    end = ()

    if command.startswith("turn on"):
        action_command = "on"
    elif command.startswith("turn off"):
        action_command = "off"
    elif command.startswith("toggle"):
        action_command = "toggle"

    coordinates = command \
        .replace("turn on ", "") \
        .replace("turn off ", "") \
        .replace("toggle ", "") \
        .split(" through ")

    start = tuple(map(int, coordinates[0].split(",")))
    end = tuple(map(int, coordinates[1].split(",")))

    return (action_command, start, end)


if __name__ == "__main__":
    with open("06_lights.lst") as file:
        lights = SimpleLights(1000, False)
        brightness_lights = LightsWithBrightnessControll(1000, 0)

        for cmd in parse_commands(file.readlines()):
            lights.execute(cmd)
            brightness_lights.execute(cmd)

        print("Number of lit lights:", lights.number_of_lit_lights)
        print("Total brightness:", brightness_lights.total_brightness)
