from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from typing import Callable, Sequence


class IO:
    def __init__(self, input):
        self.input = input
        self.output = []

    def get_input(self):
        return self.input

    def set_output(self, value):
        self.output.append(value)


class NoIO(IO):
    def __init__(self):
        super().__init__(0)


class Thruster:
    def __init__(self):
        self.value = None

    def add_input(self, value):
        self.value = value

    def set_output(self, value):
        self.value = value


class AmplificationCircuit:
    def __init__(self, program: tuple[int], sequence: Sequence[int]):
        self.program = program
        self.thruster = Thruster()

        a = Amplifier([sequence[0], 0])
        b = Amplifier([sequence[1]])
        c = Amplifier([sequence[2]])
        d = Amplifier([sequence[3]])
        e = Amplifier([sequence[4]])

        a.next_amplifier = b
        b.next_amplifier = c
        c.next_amplifier = d
        d.next_amplifier = e
        e.next_amplifier = self.thruster

        self.amplifiers = [a, b, c, d, e]

    def execute(self):
        for amp in self.amplifiers:
            cpu = Computer(amp, list(self.program))
            cpu.execute()

        return self.thruster.value


class Amplifier:
    def __init__(self, initial_input: list[int]):
        self.initial_input = initial_input
        self.next_amplifier = None

    def add_input(self, value):
        self.initial_input.append(value)

    def get_input(self):
        param = self.initial_input[0]
        self.initial_input = self.initial_input[1:]
        return param

    def set_output(self, value):
        self.next_amplifier.add_input(value)


class Computer:
    def __init__(self, io: IO, puzzle: list[int], pointer: int = 0):
        self.program = puzzle
        self.pointer = pointer
        self.io = io

    def execute_step(self):
        cmd = self.__get_command()
        return cmd.execute()

    def execute(self):
        computer = self
        try:
            while True:
                computer = computer.execute_step()
        except StopIteration:
            return computer

    def __get_command(self) -> AbstractCommand:
        PositionHandler = self.PositionParameterHandler
        ImmediateHandler = self.ImmediateParameterHandler
        full_command = format("%05d" % self.program[self.pointer])
        second_param_handler = PositionHandler(2) if full_command[1] == "0" else ImmediateHandler(2)
        first_param_handler = PositionHandler(1) if full_command[2] == "0" else ImmediateHandler(1)
        command_name = int(full_command[3:])
        commands = {
            1: self.AddCommand(self, first_param_handler, second_param_handler),
            2: self.MultiplyCommand(self, first_param_handler, second_param_handler),
            3: self.InputCommand(self),
            4: self.OutputCommand(self, first_param_handler),
            5: self.JumpIfTrueCommand(self, first_param_handler, second_param_handler),
            6: self.JumpIfFalseCommand(self, first_param_handler, second_param_handler),
            7: self.LessThanCommand(self, first_param_handler, second_param_handler),
            8: self.EqualToCommand(self, first_param_handler, second_param_handler),
            99: self.HaltCommand(self),
        }
        return commands[command_name]

    def move(self, move_offset: int) -> Computer:
        return Computer(
            self.io,
            list(self.program[:]),
            self.pointer + move_offset)

    def jump_to(self, pointer) -> Computer:
        return Computer(
            self.io,
            list(self.program[:]),
            pointer
        )

    def _set_result(self, result: int, result_position: int, move_offset: int) -> Computer:
        position = self.pointer + result_position
        result_index = self.program[position]
        updated_program = list(self.program[:])
        updated_program[result_index] = result
        updated_pointer = self.pointer + move_offset
        return Computer(self.io, updated_program, updated_pointer)

    class PositionParameterHandler:
        def __init__(self, index: int):
            self.index = index

        def __call__(self, cpu: Computer):
            position = cpu.pointer + self.index
            arg_index = cpu.program[position]
            return cpu.program[arg_index]

    class ImmediateParameterHandler:
        def __init__(self, index: int):
            self.index = index

        def __call__(self, cpu: Computer):
            position = cpu.pointer + self.index
            return cpu.program[position]

    class AbstractCommand(ABC):
        def __init__(self, cpu: Computer):
            self.cpu = cpu

        @abstractmethod
        def execute(self) -> Computer:
            pass

    class HaltCommand(AbstractCommand):
        def __init__(self, cpu):
            super().__init__(cpu)

        def execute(self) -> Computer:
            raise StopIteration

    class AbstractMathCommand(AbstractCommand):
        def __init__(self, operation: Callable[[int, int], int], cpu, arg1, arg2):
            super().__init__(cpu)
            self.operation = operation
            self.arg1 = arg1
            self.arg2 = arg2

        def execute(self) -> Computer:
            a = self.arg1(self.cpu)
            b = self.arg2(self.cpu)
            return self.cpu._set_result(
                result=self.operation(a, b),
                result_position=3,
                move_offset=4
            )

    class AddCommand(AbstractMathCommand):
        def __init__(self, cpu, arg1, arg2):
            super().__init__(lambda a, b: a + b, cpu, arg1, arg2)

    class MultiplyCommand(AbstractMathCommand):
        def __init__(self, cpu, arg1, arg2):
            super().__init__(lambda a, b: a * b, cpu, arg1, arg2)

    class InputCommand(AbstractCommand):
        def __init__(self, cpu):
            super().__init__(cpu)

        def execute(self) -> Computer:
            input_value = self.cpu.io.get_input()
            return self.cpu._set_result(input_value, 1, 2)

    class OutputCommand(AbstractCommand):
        def __init__(self, cpu, arg):
            super().__init__(cpu)
            self.arg = arg

        def execute(self):
            value = self.arg(self.cpu)
            self.cpu.io.set_output(value)
            return self.cpu.move(2)

    class AbstractJumpCommand(AbstractCommand):
        def __init__(self, condition: Callable[[int], bool], cpu, arg1, arg2):
            super().__init__(cpu)
            self.condition = condition
            self.arg1 = arg1
            self.arg2 = arg2

        def execute(self) -> Computer:
            first_param = self.arg1(self.cpu)
            if self.condition(first_param):
                new_pointer = self.arg2(self.cpu)
                return self.cpu.jump_to(new_pointer)
            else:
                return self.cpu.move(3)

    class JumpIfTrueCommand(AbstractJumpCommand):
        def __init__(self, cpu, arg1, arg2):
            super().__init__(lambda value: value != 0, cpu, arg1, arg2)

    class JumpIfFalseCommand(AbstractJumpCommand):
        def __init__(self, cpu, arg1, arg2):
            super().__init__(lambda value: value == 0, cpu, arg1, arg2)

    class AbstractLogicConditionCommand(AbstractCommand):
        def __init__(self, condition: Callable[[int, int], int], cpu, arg1, arg2):
            super().__init__(cpu)
            self.condition = condition
            self.arg1 = arg1
            self.arg2 = arg2

        def execute(self):
            arg1 = self.arg1(self.cpu)
            arg2 = self.arg2(self.cpu)
            return self.cpu._set_result(
                self.condition(arg1, arg2),
                3,
                4
            )

    class LessThanCommand(AbstractLogicConditionCommand):
        def __init__(self, cpu, arg1, arg2):
            super().__init__(lambda a, b: 1 if a < b else 0, cpu, arg1, arg2)

    class EqualToCommand(AbstractLogicConditionCommand):
        def __init__(self, cpu, arg1, arg2):
            super().__init__(lambda a, b: 1 if a == b else 0, cpu, arg1, arg2)


def run_program(current_puzzle: list[int], io: IO = NoIO()):
    return Computer(io, current_puzzle).execute().program


def find_max_thruster_signal(program):
    max_thrust = -1
    for input_sequence in itertools.permutations((0, 1, 2, 3, 4)):
        thrust = AmplificationCircuit(program, input_sequence).execute()
        max_thrust = max(thrust, max_thrust)

    return max_thrust


if __name__ == "__main__":
    puzzle = (
        3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 38, 55, 64, 89, 114, 195, 276, 357, 438, 99999, 3, 9, 101, 3, 9, 9, 102,
        3, 9, 9, 1001, 9, 5, 9, 4, 9, 99, 3, 9, 101, 2, 9, 9, 1002, 9, 3, 9, 101, 5, 9, 9, 4, 9, 99, 3, 9, 101, 3, 9, 9,
        4, 9, 99, 3, 9, 1002, 9, 4, 9, 101, 5, 9, 9, 1002, 9, 5, 9, 101, 5, 9, 9, 102, 3, 9, 9, 4, 9, 99, 3, 9, 101, 3,
        9, 9, 1002, 9, 4, 9, 101, 5, 9, 9, 102, 5, 9, 9, 1001, 9, 5, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101,
        2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2,
        9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4,
        9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9,
        3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9,
        102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 99, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9,
        102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2,
        9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 99, 3, 9, 1001, 9,
        1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9,
        4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9,
        3, 9, 101, 1, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3,
        9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9,
        1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 99
    )
    print("part 1:", find_max_thruster_signal(puzzle))
