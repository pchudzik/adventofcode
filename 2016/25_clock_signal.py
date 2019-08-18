"""
--- Day 25: Clock Signal ---

You open the door and find yourself on the roof. The city sprawls away from you for miles and miles.

There's not much time now - it's already Christmas, but you're nowhere near the North Pole, much too far to deliver
these stars to the sleigh in time.

However, maybe the huge antenna up here can offer a solution. After all, the sleigh doesn't need the stars, exactly; it
needs the timing data they provide, and you happen to have a massive signal generator right here.

You connect the stars you have to your prototype computer, connect that to the antenna, and begin the transmission.

Nothing happens.

You call the service number printed on the side of the antenna and quickly explain the situation. "I'm not sure what
kind of equipment you have connected over there," he says, "but you need a clock signal." You try to explain that this
is a signal for a clock.

"No, no, a clock signal - timing information so the antenna computer knows how to read the data you're sending it. An
endless, alternating pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.

You ask if the antenna can handle a clock signal at the frequency you would need to use for the data from the stars.
"There's no way it can! The only antenna we've installed capable of that is on top of a top-secret Easter Bunny
installation, and you're definitely not-" You hang up the phone.

You've extracted the antenna's clock signal generation assembunny code (your puzzle input); it looks mostly compatible
with code you worked on just recently.

This antenna code, being a signal generator, uses one extra instruction:

out x transmits x (either an integer or the value of a register) as the next value for the clock signal.

The code takes a value (via register a) that describes the signal to generate, but you're not sure how it's used. You'll
have to find the input to produce the right signal through experimentation.

What is the lowest positive integer that can be used to initialize register a and cause the code to output a clock
signal of 0, 1, 0, 1... repeating forever?

Your puzzle answer was 180.

--- Part Two ---

The antenna is ready. Now, all you need is the fifty stars required to generate the signal for the sleigh, but you don't
have enough.

You look toward the sky in desperation... suddenly noticing that a lone star has been installed at the top of the
antenna! Only 49 more to go.

If you like, you can.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Value:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class ClockSignalOutHandler:
    def __init__(self, expected_cycle=100):
        self.expected_cycle = expected_cycle
        self.can_continue = True
        self.result = True
        self._next_expected = 0
        self._cycle = 0

    def __call__(self, value):
        if value != self._next_expected:
            self.can_continue = False
            self.result = False
        else:
            self._cycle += 1

        self._next_expected = 1 if self._next_expected == 0 else 0
        if self._cycle >= self.expected_cycle:
            self.can_continue = False


class DoNothingHandler:
    def __init__(self):
        self.can_continue = True
        self.result = True

    def __call__(self, value):
        pass


class Cmd:
    def execute(self, cpu):
        raise NotImplementedError()


class CpyCmd(Cmd):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def execute(self, cpu):
        cpu.value(self.dst).value = cpu.value(self.src).value

    def __repr__(self):
        return f"cpy {self.src} {self.dst}"


class IncCmd(Cmd):
    def __init__(self, registry, value):
        self.registry = registry
        self.value = value

    def execute(self, cpu):
        cpu.registry[self.registry].value += self.value

    def __repr__(self):
        if self.value > 0:
            return f"inc {self.registry}"
        else:
            return f"dec {self.registry}"


class JnzCmd(Cmd):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def execute(self, cpu):
        if cpu.value(self.x).value != 0:
            cpu.move(cpu.value(self.y).value - 1)

    def __repr__(self):
        return f"jnz {self.x} {self.y}"


class OutCmd(Cmd):
    def __init__(self, value):
        self.value = value

    def execute(self, cpu):
        value = cpu.value(self.value).value
        cpu.out_handler(value)

    def __repr__(self):
        return f"out {self.value}"


class Cpu:
    def __init__(self, registry=None, out_handler=None):
        self.stack = 0
        self.out_handler = DoNothingHandler() if not out_handler else out_handler

        if not registry:
            self.registry = {
                'a': Value(0),
                'b': Value(0),
                'c': Value(0),
                'd': Value(0)
            }
        else:
            self.registry = registry

    def program(self, cmds):
        cmds = list(cmds)
        while len(cmds) > self.stack and self.out_handler.can_continue:
            cmd = cmds[self.stack]
            cmd.execute(self)
            self.stack += 1
        else:
            return self.out_handler.result

    def value(self, value):
        try:
            return Value(int(value))
        except ValueError:
            return self.registry[value]

    def move(self, step):
        self.stack += step


def parser(expression: str):
    if expression.startswith("cpy"):
        x, y = expression.replace("cpy ", "").split(" ")
        return CpyCmd(x, y)
    elif expression.startswith("inc"):
        registry = expression.replace("inc ", "")
        return IncCmd(registry, 1)
    elif expression.startswith("dec"):
        registry = expression.replace("dec ", "")
        return IncCmd(registry, -1)
    elif expression.startswith("jnz"):
        x, y = expression.replace("jnz ", "").split(" ")
        return JnzCmd(x, int(y))
    elif expression.startswith("out"):
        val = expression.replace("out ", "")
        return OutCmd(val)


def find_integer_for_clock_signal(cmds):
    number = 0
    while True:
        cpu = Cpu(
            out_handler=ClockSignalOutHandler(),
            registry={
                'a': Value(number),
                'b': Value(0),
                'c': Value(0),
                'd': Value(0)
            })
        if cpu.program(cmds):
            return number
        number += 1


if __name__ == "__main__":
    program = [parser(cmd) for cmd in [
        "cpy a d",
        "cpy 15 c",
        "cpy 170 b",
        "inc d",
        "dec b",
        "jnz b -2",
        "dec c",
        "jnz c -5",
        "cpy d a",
        "jnz 0 0",
        "cpy a b",
        "cpy 0 a",
        "cpy 2 c",
        "jnz b 2",
        "jnz 1 6",
        "dec b",
        "dec c",
        "jnz c -4",
        "inc a",
        "jnz 1 -7",
        "cpy 2 b",
        "jnz c 2",
        "jnz 1 4",
        "dec b",
        "dec c",
        "jnz 1 -4",
        "jnz 0 0",
        "out b",
        "jnz a -19",
        "jnz 1 -21",
    ]]

    print(f"part1 {find_integer_for_clock_signal(program)}")
