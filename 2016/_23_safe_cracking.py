"""
--- Day 23: Safe Cracking ---

This is one of the top floors of the nicest tower in EBHQ. The Easter Bunny's private office is here, complete with a
safe hidden behind a painting, and who wouldn't hide a star in a safe behind a painting?

The safe has a digital screen and keypad for code entry. A sticky note attached to the safe has a password hint on it:
"eggs". The painting is of a large rabbit coloring some eggs. You see 7.

When you go to type the code, though, nothing appears on the display; instead, the keypad comes apart in your hands,
apparently having been smashed. Behind it is some kind of socket - one that matches a connector in your prototype
computer! You pull apart the smashed keypad and extract the logic circuit, plug it into your computer, and plug your
computer into the safe.

Now, you just need to figure out what output the keypad would have sent to the safe. You extract the assembunny code
from the logic chip (your puzzle input).

The code looks like it uses almost the same architecture and instruction set that the monorail computer used! You should
be able to use the same assembunny interpreter for this as you did there, but with one new instruction:

tgl x toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative means
backward):

- For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
- For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
- The arguments of a toggled instruction are not affected.
- If an attempt is made to toggle an instruction outside the program, nothing happens.
- If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction,
  skip it instead.
- If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting instruction is
  not executed until the next time it is reached.

For example, given this program:

cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a

- cpy 2 a initializes register a to 2.
- The first tgl a toggles an instruction a (2) away from it, which changes the third tgl a into inc a.
- The second tgl a also modifies an instruction 2 away from it, which changes the cpy 1 a into jnz 1 a.
- The fourth line, which is now inc a, increments a to 3.
- Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions ahead, skipping the dec a instructions.

In this example, the final value in register a is 3.

The rest of the electronics seem to place the keypad entry (the number of eggs, 7) in register a, run the code, and then
send the value left in register a to the safe.

What value should be sent to the safe?

Your puzzle answer was 11130.

--- Part Two ---

The safe doesn't open, but it does make several angry noises to express its frustration.

You're quite sure your logic is working correctly, so the only other thing is... you check the painting again. As it
turns out, colored eggs are still eggs. Now you count 12.

As you run the program with this new input, the prototype computer begins to overheat. You wonder what's taking so long,
and whether the lack of any instruction more powerful than "add one" has anything to do with it. Don't bunnies usually
multiply?

Anyway, what value should actually be sent to the safe?

Your puzzle answer was 479007690.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Value:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


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


class TglCmd(Cmd):
    def __init__(self, value):
        self.value = value

    def execute(self, cpu):
        val = cpu.value(self.value).value + cpu.stack
        if val >= len(cpu.cmds):
            return

        cmd = cpu.cmds[val]
        if type(cmd) is IncCmd:
            if cmd.value > 0:
                cpu.cmds[val] = IncCmd(cmd.registry, -1)
            elif cmd.value < 0:
                cpu.cmds[val] = IncCmd(cmd.registry, 1)
        elif type(cmd) is JnzCmd:
            cpu.cmds[val] = CpyCmd(cmd.x, cmd.y)
        elif type(cmd) is CpyCmd:
            cpu.cmds[val] = JnzCmd(cmd.src, cmd.dst)
        elif type(cmd) is TglCmd:
            cpu.cmds[val] = IncCmd(self.value, 1)

    def __repr__(self):
        return f"tgl {self.value}"


class Mul(Cmd):
    def __init__(self, x, y, result):
        self.x = x
        self.y = y
        self.result = result

    def execute(self, cpu):
        res = cpu.value(self.x).value * cpu.value(self.y).value
        cpu.value(self.result).value = res


class Cpu:
    def __init__(self, cmds, registry=None):
        self.stack = 0
        self.cmds = list(cmds)
        if not registry:
            self.registry = {
                'a': Value(0),
                'b': Value(0),
                'c': Value(0),
                'd': Value(0)
            }
        else:
            self.registry = registry

    def run(self):
        while len(self.cmds) > self.stack:
            cmd = self.cmds[self.stack]
            cmd.execute(self)
            self.stack += 1

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
        return JnzCmd(x, y)
    elif expression.startswith("tgl"):
        val = expression.replace("tgl ", "")
        return TglCmd(val)
    elif expression.startswith("mul"):
        x, y, result = expression.replace("mul ", "").split(" ")
        return Mul(x, y, result)


if __name__ == "__main__":
    program = [
        "cpy a b",
        "dec b",
        "cpy a d",
        "cpy 0 a",
        "cpy b c",
        "inc a",
        "dec c",
        "jnz c -2",
        "dec d",
        "jnz d -5",
        "dec b",
        "cpy b c",
        "cpy c d",
        "dec d",
        "inc c",
        "jnz d -2",
        "tgl c",
        "cpy -16 c",
        "jnz 1 c",
        "cpy 70 c",
        "jnz 87 d",
        "inc a",
        "inc d",
        "jnz d -2",
        "inc c",
        "jnz c -5"
    ]

    program_optimized_part2 = [
        "cpy a b",
        "dec b",
        "cpy a d",
        "cpy 0 a",
        "mul b d a",
        "cpy 0 c",
        "cpy 0 c",
        "cpy 0 c",
        "cpy 0 c",
        "cpy 0 d",
        "dec b",
        "cpy b c",
        "cpy c d",
        "dec d",
        "inc c",
        "jnz d -2",
        "tgl c",
        "cpy -16 c",
        "jnz 1 c",
        "cpy 70 c",
        "jnz 87 d",
        "inc a",
        "inc d",
        "jnz d -2",
        "inc c",
        "jnz c -5"
    ]

    cpu_part1 = Cpu(
        [parser(cmd) for cmd in program],
        registry={
            'a': Value(7),
            'b': Value(0),
            'c': Value(0),
            'd': Value(0)
        })
    cpu_part2 = Cpu(
        [parser(cmd) for cmd in program_optimized_part2],
        registry={
            'a': Value(12),
            'b': Value(0),
            'c': Value(0),
            'd': Value(0)
        })

    cpu_part1.run()
    cpu_part2.run()

    print(f"part1 {cpu_part1.registry['a']}")
    print(f"part2 {cpu_part2.registry['a']}")
