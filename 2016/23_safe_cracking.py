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

    cpu_part1 = Cpu(
        [parser(cmd) for cmd in program],
        registry={
            'a': Value(7),
            'b': Value(0),
            'c': Value(0),
            'd': Value(0)
        })
    cpu_part2 = Cpu(
        [parser(cmd) for cmd in program],
        registry={
            'a': Value(12),
            'b': Value(0),
            'c': Value(0),
            'd': Value(0)
        })

    cpu_part1.run()
    # cpu_part2.run()   too slow need to optimize

    print(f"part1 {cpu_part1.registry['a']}")
    print(f"part1 {cpu_part2.registry['a']}")
