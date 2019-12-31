"""
--- Day 18: Duet ---

You discover a tablet containing some strange assembly code labeled simply "Duet". Rather than bother the sound card
with it, you decide to run the code yourself. Unfortunately, you don't see any documentation, so you're left to figure
out what the instructions mean on your own.

It seems like the assembly is meant to operate on a set of registers that are each named with a single letter and that
can each hold a single integer. You suppose each register should start with a value of 0.

There aren't that many instructions, so it shouldn't be hard to figure out what they do. Here's what you determine:

* snd X plays a sound with a frequency equal to the value of X.
* set X Y sets register X to the value of Y.
* add X Y increases register X by the value of Y.
* mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
* mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it
  sets X to the result of X modulo Y).
* rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the
  command does nothing.)
* jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips
  the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

Many of the instructions can take either a register (a single letter) or a number. The value of a register is the
integer it contains; the value of a number is that number.

After each jump instruction, the program continues with the instruction to which the jump jumped. After any other
instruction, the program continues with the next instruction. Continuing (or jumping) off either end of the program
terminates it.

For example:

set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2

* The first four instructions set a to 1, add 2 to it, square it, and then set it to itself modulo 5, resulting in a
  value of 4.
* Then, a sound with frequency 4 (the value of a) is played.
* After that, a is set to 0, causing the subsequent rcv and jgz instructions to both be skipped (rcv because a is 0, and
  jgz because a is not greater than 0).
* Finally, a is set to 1, causing the next jgz instruction to activate, jumping back two instructions to another jump,
  which jumps again to the rcv, which ultimately triggers the recover operation.

At the time the recover operation is executed, the frequency of the last sound played is 4.

What is the value of the recovered frequency (the value of the most recently played sound) the first time a rcv
instruction is executed with a non-zero value?

Your puzzle answer was 7071.

--- Part Two ---

As you congratulate yourself for a job well done, you notice that the documentation has been on the back of the tablet
this entire time. While you actually got most of the instructions correct, there are a few key differences. This
assembly code isn't about sound at all - it's meant to be run twice at the same time.

Each running copy of the program has its own set of registers and follows the code independently - in fact, the programs
don't even necessarily run at the same speed. To coordinate, they use the send (snd) and receive (rcv) instructions:

* snd X sends the value of X to the other program. These values wait in a queue until that program is ready to receive
  them. Each program has its own message queue, so a program can never receive a message it sent.
* rcv X receives the next value and stores it in register X. If no values are in the queue, the program waits for a
  value to be sent to it. Programs do not continue to the next instruction until they have received a value. Values are
  received in the order they are sent.

Each program also has its own program ID (one 0 and the other 1); the register p should begin with this value.

For example:

snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d

Both programs begin by sending three values to the other. Program 0 sends 1, 2, 0; program 1 sends 1, 2, 1. Then, each
program receives a value (both 1) and stores it in a, receives another value (both 2) and stores it in b, and then each
receives the program ID of the other program (program 0 receives 1; program 1 receives 0) and stores it in c. Each
program now sees a different value in its own copy of register c.

Finally, both programs try to rcv a fourth time, but no data is waiting for either of them, and they reach a deadlock.
When this happens, both programs terminate.

It should be noted that it would be equally valid for the programs to run at different speeds; for example, program 0
might have sent all three values and then stopped at the first rcv before program 1 executed even its first instruction.

Once both of your programs have terminated (regardless of what caused them to do so), how many times did program 1 send
a value?

Your puzzle answer was 8001.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Register:
    def __init__(self, value):
        self.value = value


class PersistentRegister(Register):
    def __init__(self, name, value):
        self.name = name
        self.value = value


def execute_part1(cmds):
    snd_card = Register(None)
    cmds = parser1(snd_card, cmds)
    cpu = CPU(cmds)

    execute = True
    while execute:
        try:
            execute = cpu.tick()
        except StopIteration:
            return snd_card.value


def execute_part2(cmds):
    queues = {
        0: [],
        1: []
    }
    counters = {
        0: Register(0),
        1: Register(0)
    }

    cmds_p0 = parser2(cmds, counters[0], queues[1], queues[0])
    cmds_p1 = parser2(cmds, counters[1], queues[0], queues[1])
    ctx = Orchestrator(
        CPU(cmds_p0, {"p": 0}),
        CPU(cmds_p1, {"p": 1}))

    while True:
        try:
            ctx.next_tick()
        except StopIteration:
            return counters[1].value


class Orchestrator:
    def __init__(self, cpu0, cpu1):
        self.current = {
            "cpu": cpu0,
            "status": "running",
            "id": 0
        }
        self.other = {
            "cpu": cpu1,
            "status": "running",
            "id": 1
        }

    def next_tick(self):
        if self.is_done():
            raise StopIteration

        try:
            result = self.current["cpu"].tick()
            self.current["status"] = "running"
            if not result:
                self.current["status"] = "done"
                self.swap()
        except IndexError:
            self.lock()
            self.swap()

    def is_done(self):
        return all(map(lambda c: c["status"] in ["locked", "done"], (self.current, self.other)))

    def swap(self):
        self.current, self.other = self.other, self.current

    def lock(self):
        self.current["status"] = "locked" if self.current["status"] == "waiting" else "waiting"


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


class RcvCmd2(Cmd):
    def __init__(self, queue, x):
        self.queue = queue
        self.x = x

    def _execute(self, cpu):
        value = self.queue.pop(0)
        cpu[self.x].value = value


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
    def __init__(self, snd_card, x):
        self.x = x
        self.snd_card = snd_card

    def _execute(self, cpu):
        value = cpu[self.x].value
        if value > 0:
            self.snd_card.value = value


class SndCmd2(Cmd):
    def __init__(self, queue, counter, x):
        self.queue = queue
        self.counter = counter
        self.x = x

    def _execute(self, cpu):
        self.queue.append(cpu[self.x].value)
        self.counter.value += 1


def parser1(snd_card, cmds):
    def create_snd_cmd(cmd, cmd_name):
        x = cmd.replace(f"{cmd_name} ", "")
        return SndCmd(snd_card, x)

    def create_rcv_cmd(cmd, cmd_name):
        x = cmd.replace(f"{cmd_name} ", "")
        return RcvCmd(x)

    parsers = _create_cmd_parsers()
    parsers["snd"] = create_snd_cmd
    parsers["rcv"] = create_rcv_cmd

    return parse_cmd(cmds, parsers)


def parser2(cmds, counter, snd_queue, rcv_queue):
    parsers = _create_cmd_parsers()

    def create_snd2_cmd(cmd, cmd_name):
        x = cmd.replace(f"{cmd_name} ", "")
        return SndCmd2(snd_queue, counter, x)

    def create_rcv2_cmd(cmd, cmd_name):
        x = cmd.replace(f"{cmd_name} ", "")
        return RcvCmd2(rcv_queue, x)

    parsers["snd"] = create_snd2_cmd
    parsers["rcv"] = create_rcv2_cmd

    return parse_cmd(cmds, parsers)


def _create_cmd_parsers():
    def double_arg_cmd_creator(CommandFactory):
        def create(cmd, cmd_name):
            x, y, *_ = cmd.replace(f"{cmd_name} ", "").split(" ")
            return CommandFactory(x, y)

        return create

    return {
        "set": double_arg_cmd_creator(SetCmd),
        "add": double_arg_cmd_creator(AddCmd),
        "mul": double_arg_cmd_creator(MulCmd),
        "mod": double_arg_cmd_creator(ModCmd),
        "jgz": double_arg_cmd_creator(JgzCmd)
    }


def parse_cmd(cmds, parsers):
    result = []

    for cmd in cmds:
        cmd_name = cmd.split(" ", 1)[0]
        result.append(parsers[cmd_name](cmd, cmd_name))

    return result


if __name__ == "__main__":
    with open("18_duet.txt") as file:
        cmds = list(map(str.strip, file.readlines()))

        print(f"part 1: {execute_part1(cmds)}")
        print(f"part 2: {execute_part2(cmds)}")
