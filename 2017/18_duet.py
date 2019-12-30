class Register:
    def __init__(self, value):
        self.value = value


class PersistentRegister(Register):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class CPU:
    def __init__(self, program):
        self.registers = dict()
        self.offset = 0
        self.program = program
        self.played = None

    def __getitem__(self, item):
        if item.replace("-", "").isnumeric():
            return Register(int(item))

        register = self.registers.get(item)

        if not register:
            register = PersistentRegister(item, 0)
            self.registers[item] = register

        return register

    def execute(self):
        exec = True
        while exec:
            exec = self.tick()

    def tick(self):
        if self.offset >= len(self.program):
            return False

        cmd = self.program[self.offset]

        try:
            cmd(self)
            self.offset += 1
        except StopIteration:
            return False

        return True

    def jump(self, value):
        self.offset += value


class Cmd:
    def _execute(self, cpu):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        cpu = args[0]
        self._execute(cpu)


class AddCmd(Cmd):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _execute(self, cpu):
        cpu[self.x].value += cpu[self.y].value


class MulCmd(Cmd):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _execute(self, cpu):
        cpu[self.x].value *= cpu[self.y].value


class ModCmd(Cmd):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _execute(self, cpu):
        cpu[self.x].value %= cpu[self.y].value


class RcvCmd(Cmd):
    def __init__(self, x):
        self.x = x

    def _execute(self, cpu):
        value = cpu[self.x].value
        if value > 0:
            cpu.received = value
            raise StopIteration


class JgzCmd(Cmd):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _execute(self, cpu):
        value = cpu[self.x].value
        if value > 0:
            jump_offset = cpu[self.y].value
            cpu.jump(jump_offset - 1)


class SetCmd(Cmd):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _execute(self, cpu):
        cpu[self.x].value = cpu[self.y].value


class SndCmd(Cmd):
    def __init__(self, x):
        self.x = x

    def _execute(self, cpu):
        value = cpu[self.x].value
        if value > 0:
            cpu.played = value


def parser(cmds):
    result = []

    def double_arg_cmd_creator(CommandFactory):
        def create(cmd, cmd_name):
            x, y, *_ = cmd.replace(f"{cmd_name} ", "").split(" ")
            return CommandFactory(x, y)

        return create

    def single_arg_cmd_creator(CommandFactory):
        def create(cmd, cmd_name):
            x = cmd.replace(f"{cmd_name} ", "")
            return CommandFactory(x)

        return create

    parsers = {
        "set": double_arg_cmd_creator(SetCmd),
        "add": double_arg_cmd_creator(AddCmd),
        "mul": double_arg_cmd_creator(MulCmd),
        "mod": double_arg_cmd_creator(ModCmd),
        "jgz": double_arg_cmd_creator(JgzCmd),
        "rcv": single_arg_cmd_creator(RcvCmd),
        "snd": single_arg_cmd_creator(SndCmd)
    }

    for cmd in cmds:
        cmd_name = cmd.split(" ", 1)[0]
        result.append(parsers[cmd_name](cmd, cmd_name))

    return result


if __name__ == "__main__":
    with open("18_duet.txt") as file:
        cmds = parser(map(str.strip, file.readlines()))
        cpu = CPU(cmds)

        cpu.execute()

        print(f"part 1: {cpu.played}")
