"""
-- Day 12: Leonardo's Monorail ---

You finally reach the top floor of this building: a garden with a slanted glass ceiling. Looks like there are no more
stars to be had.

While sitting on a nearby bench amidst some tiger lilies, you manage to decrypt some of the files you extracted from the
servers downstairs.

According to these documents, Easter Bunny HQ isn't just this building - it's a collection of buildings in the nearby
area. They're all connected by a local monorail, and there's another building not far from here! Unfortunately, being
night, the monorail is currently not operating.

You remotely connect to the monorail control systems and discover that the boot sequence expects a password. The
password-checking logic (your puzzle input) is easy to extract, but the code it uses is strange: it's assembunny code
designed for the new computer you just assembled. You'll have to execute the code and get the password.

The assembunny code you've extracted operates on four registers (a, b, c, and d) that start at 0 and can hold any
integer. However, it seems to make use of only a few instructions:

cpy x y copies x (either an integer or the value of a register) into register y.
inc x increases the value of register x by one.
dec x decreases the value of register x by one.
jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.
The jnz instruction moves relative to itself: an offset of -1 would continue at the previous instruction, while an
offset of 2 would skip over the next instruction.

For example:

cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a

The above code would set register a to 41, increase its value by 2, decrease its value by 1, and then skip the last dec
a (because a is not zero, so the jnz a 2 skips it), leaving register a at 42. When you move past the last instruction,
the program halts.

After executing the assembunny code in your puzzle input, what value is left in register a?

Your puzzle answer was 318009.

--- Part Two ---

As you head down the fire escape to the monorail, you notice it didn't start; register c needs to be initialized to the
position of the ignition key.

If you instead initialize register c to be 1, what value is now left in register a?

Your puzzle answer was 9227663.

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


class Cpu:
    def __init__(self, registry=None):
        self.stack = 0
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
        while len(cmds) > self.stack:
            cmd = cmds[self.stack]
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
        return JnzCmd(x, int(y))


if __name__ == "__main__":
    cpu_part1 = Cpu()
    cpu_part2 = Cpu({
        'a': Value(0),
        'b': Value(0),
        'c': Value(1),
        'd': Value(0)
    })
    program = [
        "cpy 1 a",
        "cpy 1 b",
        "cpy 26 d",
        "jnz c 2",
        "jnz 1 5",
        "cpy 7 c",
        "inc d",
        "dec c",
        "jnz c -2",
        "cpy a c",
        "inc a",
        "dec b",
        "jnz b -2",
        "cpy c b",
        "dec d",
        "jnz d -6",
        "cpy 18 c",
        "cpy 11 d",
        "inc a",
        "dec d",
        "jnz d -2",
        "dec c",
        "jnz c -5"
    ]

    cpu_part1.program(parser(cmd) for cmd in program)
    cpu_part2.program(parser(cmd) for cmd in program)

    print(f"part1 {cpu_part1.registry['a']}")
    print(f"part2 {cpu_part2.registry['a']}")
