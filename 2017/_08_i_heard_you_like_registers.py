"""
--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you
to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's
value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction
without modifying the register. The registers all start at 0. The instructions look like this:
* b inc 5 if a > 1
* a inc 1 if b < 5
* c dec -10 if a >= 1
* c inc -20 if c == 10

These instructions would be processed as follows:
* Because a starts at 0, it is not greater than 1, and so b is not modified.
* a is increased by 1 (to 1) because b is less than 5 (it is 0).
* c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
* c is increased by -20 (to -10) because c is equal to 10.

After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth to
tell you what all the registers are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?

Your puzzle answer was 2971.

--- Part Two ---

To be safe, the CPU also needs to know the highest value held in any register during this process so that it can decide
how much memory to allocate to these operations. For example, in the above instructions, the highest value ever held was
10 (in register c after the third instruction was evaluated).

Your puzzle answer was 4254.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

import re
from collections import defaultdict

instruction_pattern = re.compile(r"^([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) ([=><!]{1,2}) (-?\d+)$")


class _Program:
    def __init__(self, register, action, condition_register, condition):
        self.register = register
        self.action = action
        self.condition_register = condition_register
        self.condition = condition


class CPU:
    def __init__(self):
        self.registers = defaultdict(int)
        self.max_ever = 0

    def execute(self, program):
        current_value = self.registers[program.register]
        if program.condition(self.registers[program.condition_register]):
            self.registers[program.register] = program.action(current_value)

        max_value = max(self.registers.values())
        if self.max_ever < max_value:
            self.max_ever = max_value


def parse_instruction(instruction):
    match = instruction_pattern.match(instruction)
    if not match:
        raise ValueError(f"{instruction} doesn't match program pattern")

    register = match.group(1)
    sign = 1 if match.group(2) == "inc" else -1
    value = int(match.group(3)) * sign
    action = lambda val: val + value

    condition_register = match.group(4)
    condition_operator = match.group(5)
    condition_value = int(match.group(6))
    conditions = {
        "==": lambda val: val == condition_value,
        "!=": lambda val: val != condition_value,
        ">": lambda val: val > condition_value,
        "<": lambda val: val < condition_value,
        ">=": lambda val: val >= condition_value,
        "<=": lambda val: val <= condition_value
    }

    return _Program(register, action, condition_register, conditions[condition_operator])


def run_program(instructions):
    cpu = CPU()
    program = [parse_instruction(instruction) for instruction in instructions]
    for operation in program:
        cpu.execute(operation)

    return cpu


if __name__ == "__main__":
    with open("_08_i_heard_you_like_registers.txt") as file:
        cpu = run_program(line.strip() for line in file.readlines())

        max_value = max(cpu.registers.values())

        print(f"part1: {max_value}")
        print(f"part2: {cpu.max_ever}")
