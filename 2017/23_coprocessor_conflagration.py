"""
--- Day 23: Coprocessor Conflagration ---

You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental
coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause serious
issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality seems
very similar, but some of the instructions are different:

* set X Y sets register X to the value of Y.
* sub X Y decreases register X by the value of Y.
* mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
* jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the next
  instruction, an offset of -1 jumps to the previous instruction, and so on.)

Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing any
meaningful work.

If you run the program (your puzzle input), how many times is the mul instruction invoked?

Your puzzle answer was 5929.

--- Part Two ---

Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch, which makes register a now start at 1 when
the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose a very efficient
implementation. You'll need to optimize the program if it has any hope of completing before Santa needs that printer
working.

The coprocessor's ultimate goal is to determine the final value left in register h once the program completes.
Technically, if it had that... it wouldn't even need to run the program.

After setting register a to 1, if the program were to run to completion, what value would be left in register h?

Your puzzle answer was 907.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Register:
    def __init__(self, value):
        self.value = value


class PersistentRegister(Register):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class CPU:
    def __init__(self, program, initial_registers=None):
        if initial_registers is not None:
            self.registers = {n: PersistentRegister(n, v) for n, v in initial_registers.items()}
        else:
            self.registers = dict()

        self.offset = 0
        self.program = program

    def __getitem__(self, item):
        if item.replace("-", "").isnumeric():
            return Register(int(item))

        register = self.registers.get(item)

        if not register:
            register = PersistentRegister(item, 0)
            self.registers[item] = register

        return register

    def tick(self):
        if self.offset >= len(self.program):
            return False

        cmd = self.program[self.offset]

        cmd(self)
        self.offset += 1

        return True

    def jump(self, value):
        self.offset += value


def execute(cmds, registers=None):
    cpu = CPU(cmds, initial_registers=registers)

    execute = True
    while execute:
        execute = cpu.tick()

    return cpu


class Cmd:
    def __init__(self, callback, cmd_name):
        self.callback = callback
        self.cmd_name = cmd_name

    def _execute(self, cpu):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        cpu = args[0]
        self._execute(cpu)
        self.callback(self.cmd_name)


class SetCmd(Cmd):
    def __init__(self, callback, x, y):
        Cmd.__init__(self, callback, "set")
        self.x = x
        self.y = y

    def _execute(self, cpu):
        cpu[self.x].value = cpu[self.y].value


class SubCmd(Cmd):
    def __init__(self, callback, x, y):
        Cmd.__init__(self, callback, "sub")
        self.x = x
        self.y = y

    def _execute(self, cpu):
        cpu[self.x].value -= cpu[self.y].value


class MulCmd(Cmd):
    def __init__(self, callback, x, y):
        Cmd.__init__(self, callback, "mul")
        self.x = x
        self.y = y

    def _execute(self, cpu):
        cpu[self.x].value *= cpu[self.y].value


class JnzCmd(Cmd):
    def __init__(self, callback, x, y):
        Cmd.__init__(self, callback, "jnz")
        self.x = x
        self.y = y

    def _execute(self, cpu):
        value = cpu[self.x].value
        if value != 0:
            jump_offset = cpu[self.y].value
            cpu.jump(jump_offset - 1)


def parser(callback, cmds):
    parsers = _create_cmd_parsers(callback)

    return parse_cmd(cmds, parsers)


def _create_cmd_parsers(callback):
    def double_arg_cmd_creator(CommandFactory):
        def create(cmd, cmd_name):
            x, y, *_ = cmd.replace(f"{cmd_name} ", "").split(" ")
            return CommandFactory(callback, x, y)

        return create

    return {
        "set": double_arg_cmd_creator(SetCmd),
        "sub": double_arg_cmd_creator(SubCmd),
        "mul": double_arg_cmd_creator(MulCmd),
        "jnz": double_arg_cmd_creator(JnzCmd)
    }


def parse_cmd(cmds, parsers):
    result = []

    for cmd in cmds:
        cmd_name = cmd.split(" ", 1)[0]
        result.append(parsers[cmd_name](cmd, cmd_name))

    return result


class MulCountingCallback:
    def __init__(self):
        self.count = 0

    def __call__(self, *args, **kwargs):
        cmd = args[0]
        if cmd == "mul":
            self.count += 1


def part2(initial_b):
    h = 0
    start = initial_b * 100 + 100000
    end = start + 17000 + 1

    for x in range(start, end, 17):
        for i in range(2, x):
            if x % i == 0:
                h += 1
                break

    return h


if __name__ == "__main__":
    with open("23_coprocessor_conflagration.txt") as file:
        mul_counter = MulCountingCallback()
        cmds = list(map(str.strip, file.readlines()))
        cmds = parser(mul_counter, cmds)
        execute(cmds)
        print(f"part 1: {mul_counter.count}")
        print(f"part 2: {part2(79)}")
