"""
--- Day 16: Chronal Classification ---

As you see the Elves defend their hot chocolate successfully, you go back to falling through time. This is going to
become a problem.

If you're ever going to return to your own time, you need to understand how this device on your wrist works. You have a
little while before you reach your next destination, and with a bit of trial and error, you manage to pull up a
programming manual on the device's tiny screen.

According to the manual, the device has four registers (numbered 0 through 3) that can be manipulated by instructions
containing one of 16 opcodes. The registers start with the value 0.

Every instruction consists of four values: an opcode, two inputs (named A and B), and an output (named C), in that
order. The opcode specifies the behavior of the instruction and how the inputs are interpreted. The output, C, is always
treated as a register.

In the opcode descriptions below, if something says "value A", it means to take the number given as A literally. (This
is also called an "immediate" value.) If something says "register A", it means to use the number given as A to read from
(or write to) the register with that number. So, if the opcode addi adds register A and value B, storing the result in
register C, and the instruction addi 0 7 3 is encountered, it would add 7 to the value contained by register 0 and store
the sum in register 3, never modifying registers 0, 1, or 2 in the process.

Many opcodes are similar except for how they interpret their arguments. The opcodes fall into seven general categories:

Addition:
addr (add register) stores into register C the result of adding register A and register B.
addi (add immediate) stores into register C the result of adding register A and value B.

Multiplication:
mulr (multiply register) stores into register C the result of multiplying register A and register B.
muli (multiply immediate) stores into register C the result of multiplying register A and value B.

Bitwise AND:
banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.

Bitwise OR:
borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.

Assignment:
setr (set register) copies the contents of register A into register C. (Input B is ignored.)
seti (set immediate) stores value A into register C. (Input B is ignored.)

Greater-than testing:
gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.

Equality testing:
eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.

Unfortunately, while the manual gives the name of each opcode, it doesn't seem to indicate the number. However, you can monitor the CPU to see the contents of the registers before and after instructions are executed to try to work them out. Each opcode has a number from 0 through 15, but the manual doesn't say which is which. For example, suppose you capture the following sample:

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

This sample shows the effect of the instruction 9 2 1 2 on the registers. Before the instruction is executed, register 0
has value 3, register 1 has value 2, and registers 2 and 3 have value 1. After the instruction is executed, register 2's
value becomes 2.

The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2, B=1, and C=2. Opcode 9 could be any of the
16 opcodes listed above, but only three of them behave in a way that would cause the result shown in the sample:

* Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1 (which has a value of 2) produces 2,
  which matches the value stored in the output register, register 2.
* Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1 produces 2, which matches the value stored in
  the output register, register 2.
* Opcode 9 could be seti: value 2 matches the value stored in the output register, register 2; the number given for B is
 irrelevant.

None of the other opcodes produce the result captured in the sample. Because of this, the sample above behaves like
three opcodes.

You collect many of these samples (the first section of your puzzle input). The manual also includes a small test
program (the second section of your puzzle input) - you can ignore it for now.

Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?

Your puzzle answer was 618.

--- Part Two ---

Using the samples you collected, work out the number of each opcode and execute the test program (the second section of
your puzzle input).

What value is contained in register 0 after executing the test program?

Your puzzle answer was 514.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

import re
from collections import namedtuple, defaultdict
from enum import Enum
from typing import List


class Cpu:
    def __init__(self, registers):
        self.registers = registers

    def execute(self, cmd):
        cmd(self.registers)

    def __str__(self):
        return f"{self.registers}"


class Value:
    def __init__(self, value):
        self.value = value

    def __call__(self, registers: dict) -> int:
        raise NotImplementedError()


class ValueI(Value):
    def __call__(self, registers: dict) -> int:
        return self.value


class ValueR(Value):
    def __call__(self, registers: dict) -> int:
        return registers[self.value]


class ValueIgnored(Value):
    def __call__(self, registers: dict) -> int:
        return None


class Cmd:
    def __init__(self, name: str, opcode: int, value_a: Value, value_b: Value, result_register: int, operation):
        self.name = name
        self.opcode = opcode
        self.value_a = value_a
        self.value_b = value_b
        self.operation = operation
        self.result_register = result_register

    def __call__(self, registers: dict) -> None:
        a = self.value_a(registers)
        b = self.value_b(registers)
        registers[self.result_register] = self.operation(a, b)

    def __str__(self):
        return f"{self.name} {self.value_a} {self.value_b} {self.result_register}"


CmdFactory = namedtuple("CmdFactory", "name, value_a, value_b, operation")


class Cmds(Enum):
    addr = CmdFactory(name="addr", value_a=ValueR, value_b=ValueR, operation=lambda a, b: a + b)
    addi = CmdFactory(name="addi", value_a=ValueR, value_b=ValueI, operation=lambda a, b: a + b)
    mulr = CmdFactory(name="mulr", value_a=ValueR, value_b=ValueR, operation=lambda a, b: a * b)
    muli = CmdFactory(name="muli", value_a=ValueR, value_b=ValueI, operation=lambda a, b: a * b)
    banr = CmdFactory(name="banr", value_a=ValueR, value_b=ValueR, operation=lambda a, b: a & b)
    bani = CmdFactory(name="bani", value_a=ValueR, value_b=ValueI, operation=lambda a, b: a & b)
    borr = CmdFactory(name="borr", value_a=ValueR, value_b=ValueR, operation=lambda a, b: a | b)
    bori = CmdFactory(name="bori", value_a=ValueR, value_b=ValueI, operation=lambda a, b: a | b)
    setr = CmdFactory(name="setr", value_a=ValueR, value_b=ValueIgnored, operation=lambda a, b: a)
    seti = CmdFactory(name="seti", value_a=ValueI, value_b=ValueIgnored, operation=lambda a, b: a)
    gtir = CmdFactory(name="gtir", value_a=ValueI, value_b=ValueR, operation=lambda a, b: 1 if a > b else 0)
    gtri = CmdFactory(name="gtri", value_a=ValueR, value_b=ValueI, operation=lambda a, b: 1 if a > b else 0)
    gtrr = CmdFactory(name="gtrr", value_a=ValueR, value_b=ValueR, operation=lambda a, b: 1 if a > b else 0)
    eqir = CmdFactory(name="eqir", value_a=ValueI, value_b=ValueR, operation=lambda a, b: 1 if a == b else 0)
    eqri = CmdFactory(name="eqri", value_a=ValueR, value_b=ValueI, operation=lambda a, b: 1 if a == b else 0)
    eqrr = CmdFactory(name="eqrr", value_a=ValueR, value_b=ValueR, operation=lambda a, b: 1 if a == b else 0)


def create_cmd(operation: List[int], cmd: Cmds):
    opcode = operation[0]
    value_a = cmd.value.value_a(operation[1])
    value_b = cmd.value.value_b(operation[2])
    result_register = operation[3]
    return Cmd(cmd.value.name, opcode, value_a, value_b, result_register, cmd.value.operation)


def op_code_parser(lines: List[str]):
    before_after_regex = re.compile(r"\w+:\s+\[(\d+),\s(\d+),\s(\d+),\s(\d+)\]")
    before, operation, after = lines
    before = [int(x) for x in before_after_regex.match(before).groups()]
    after = [int(x) for x in before_after_regex.match(after).groups()]
    operation = [int(x) for x in operation.split()]

    return before, operation, after


def resolve_possible_commands(single_step: List[str]):
    before, operation, after = op_code_parser(single_step)
    matched_commands = []
    for cmd in Cmds:
        cpu = Cpu(list(before))
        cmd_to_run = create_cmd(operation, cmd)
        cpu.execute(cmd_to_run)
        if cpu.registers == after:
            matched_commands.append((cmd, cmd_to_run.opcode))

    return matched_commands


def part1(input):
    result = 0
    for lines in input:
        lines = [l.strip() for l in lines.split("\n")]
        matched_opcodes = len(resolve_possible_commands(lines))
        if matched_opcodes >= 3:
            result += 1
    return result


def find_opcode_commands(input):
    opcode_to_cmd = defaultdict(set)
    for lines in input:
        lines = [l.strip() for l in lines.split("\n")]
        for cmd, opcode in resolve_possible_commands(lines):
            opcode_to_cmd[opcode].add(cmd.name)

    found_commands = {}
    while len(found_commands) != len(Cmds):
        comands_with_single_opcode = [
            (opcode, list(cmds)[0])
            for opcode, cmds in opcode_to_cmd.items()
            if len(cmds) == 1
        ]
        for opcode, cmd in comands_with_single_opcode:
            found_commands[opcode] = cmd
            for opcode, cmds in opcode_to_cmd.items():
                opcode_to_cmd[opcode] = {possible_cmd for possible_cmd in cmds if possible_cmd != cmd}

    return found_commands


def part2(input1, input2):
    opcodes = find_opcode_commands(input1)
    registers = run_program(input2, opcodes)
    return registers[0]


def run_program(program, commands_dictionary):
    cpu = Cpu([0, 0, 0, 0])
    for index, line in enumerate(program):
        opcode, a, b, result_register = [int(x) for x in line.split()]
        cmd = Cmds[commands_dictionary[opcode]]
        a = cmd.value.value_a(a)
        b = cmd.value.value_b(b)
        cmd_to_execute = Cmd(cmd.name, opcode, a, b, result_register, cmd.value.operation)
        cpu.execute(cmd_to_execute)
    return cpu.registers


if __name__ == "__main__":
    with open("_16_chronal_classification.part_1.txt") as part1_puzzle, \
            open("_16_chronal_classification.part_2.txt") as part2_puzzle:
        samples = part1_puzzle.read().split("\n\n")
        program = [l.strip() for l in part2_puzzle.readlines()]

        result_part1 = part1(samples)
        print(f"part 1: {result_part1}")
        print(f"part 2: {part2(samples, program)}")
