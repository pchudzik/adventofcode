from collections import defaultdict
import re

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
    with open("08_i_heard_you_like_registers.txt") as file:
        cpu = run_program(line.strip() for line in file.readlines())

        max_value = max(cpu.registers.values())

        print(f"part1: {max_value}")
        print(f"part2: {cpu.max_ever}")
