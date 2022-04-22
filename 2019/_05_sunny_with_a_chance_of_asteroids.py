from __future__ import annotations

from abc import ABC, abstractmethod


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


class Computer:
    def __init__(self, io: IO, puzzle: list[int], pointer: int = 0):
        self.program = puzzle
        self.pointer = pointer
        self.io = io

    def execute(self):
        computer = self
        try:
            while True:
                cmd = computer.__get_command()
                computer = cmd.execute()
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
            99: self.HaltCommand(self),
        }
        return commands[command_name]

    def move(self, move_offset: int) -> Computer:
        return Computer(
            self.io,
            list(self.program[:]),
            self.pointer + move_offset)

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

    class AddCommand(AbstractCommand):
        def __init__(self, cpu, arg1, arg2):
            super().__init__(cpu)
            self.arg1 = arg1
            self.arg2 = arg2

        def execute(self) -> Computer:
            a = self.arg1(self.cpu)
            b = self.arg2(self.cpu)
            return self.cpu._set_result(result=a + b, result_position=3, move_offset=4)

    class MultiplyCommand(AbstractCommand):
        def __init__(self, cpu, arg1, arg2):
            super().__init__(cpu)
            self.arg1 = arg1
            self.arg2 = arg2

        def execute(self) -> Computer:
            a = self.arg1(self.cpu)
            b = self.arg2(self.cpu)
            return self.cpu._set_result(result=a * b, result_position=3, move_offset=4)

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


def run_program(current_puzzle: list[int], io: IO = NoIO()):
    return Computer(io, current_puzzle).execute().program


def part1(current_puzzle):
    io = IO(1)
    run_program(current_puzzle, io)
    return io.output[-1]


if __name__ == "__main__":
    with open("_05_sunny_with_a_chance_of_asteroids.txt") as file:
        puzzle = [int(n) for n in "\n".join(file.readlines()).split(",")]
        print("part 1:", part1(list(puzzle)))
