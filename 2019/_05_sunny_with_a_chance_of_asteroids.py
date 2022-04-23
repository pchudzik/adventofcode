"""
--- Day 5: Sunny with a Chance of Asteroids ---

You're starting to sweat as the ship makes its way toward Mercury. The Elves suggest that you get the air conditioner
working by upgrading your ship computer to support the Thermal Environment Supervision Terminal.

The Thermal Environment Supervision Terminal (TEST) starts by running a diagnostic program (your puzzle input). The TEST
diagnostic program will run on your existing Intcode computer after a few modifications:

First, you'll need to add two new instructions:

Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the
instruction 3,50 would take an input value and store it at address 50.

Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address
50.

Programs that use these instructions will come with documentation that explains what should be connected to the input
and output. The program 3,0,4,0,99 outputs whatever it gets as input, then halts.

Second, you'll need to add support for parameter modes:

Each parameter of an instruction is handled based on its parameter mode. Right now, your ship computer already
understands parameter mode 0, position mode, which causes the parameter to be interpreted as a position - if the
parameter is 50, its value is the value stored at address 50 in memory. Until now, all parameters have been in position
mode.

Now, your ship computer will also need to handle parameters in mode 1, immediate mode. In immediate mode, a parameter is
interpreted as a value - if the parameter is 50, its value is simply 50.

Parameter modes are stored in the same value as the instruction's opcode. The opcode is a two-digit number based only on
the ones and tens digit of the value, that is, the opcode is the rightmost two digits of the first value in an
instruction. Parameter modes are single digits, one per parameter, read right-to-left from the opcode: the first
parameter's mode is in the hundreds digit, the second parameter's mode is in the thousands digit, the third parameter's
mode is in the ten-thousands digit, and so on. Any missing modes are 0.

For example, consider the program 1002,4,3,4,33.

The first instruction, 1002,4,3,4, is a multiply instruction - the rightmost two digits of the first value, 02, indicate
opcode 2, multiplication. Then, going right to left, the parameter modes are 0 (hundreds digit), 1 (thousands digit),
and 0 (ten-thousands digit, not present and therefore zero):

ABCDE
 1002

DE - two-digit opcode,      02 == opcode 2
 C - mode of 1st parameter,  0 == position mode
 B - mode of 2nd parameter,  1 == immediate mode
 A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero

This instruction multiplies its first two parameters. The first parameter, 4 in position mode, works like it did before
- its value is the value stored at address 4 (33). The second parameter, 3 in immediate mode, simply has value 3. The
result of this operation, 33 * 3 = 99, is written according to the third parameter, 4 in position mode, which also works
like it did before - 99 is written to address 4.

Parameters that an instruction writes to will never be in immediate mode.

Finally, some notes:

It is important to remember that the instruction pointer should increase by the number of values in the instruction
after the instruction finishes. Because of the new instructions, this amount is no longer always 4.

Integers can be negative: 1101,100,-1,4,0 is a valid program (find 100 + -1, store the result in position 4).

The TEST diagnostic program will start by requesting from the user the ID of the system to test by running an input
instruction - provide it 1, the ID for the ship's air conditioner unit.

It will then perform a series of diagnostic tests confirming that various parts of the Intcode computer, like parameter
modes, function correctly. For each test, it will run an output instruction indicating how far the result of the test
was from the expected value, where 0 means the test was successful. Non-zero outputs mean that a function is not working
correctly; check the instructions that were run before the output instruction to see which one failed.

Finally, the program will output a diagnostic code and immediately halt. This final output isn't an error; an output
followed immediately by a halt means the program finished. If all outputs were zero except the diagnostic code, the
diagnostic program ran successfully.

After providing 1 to the only input instruction and passing all the tests, what diagnostic code does the program
produce?

Your puzzle answer was 6761139.

--- Part Two ---

The air conditioner comes online! Its cold air feels good for a while, but then the TEST alarms start to go off. Since
the air conditioner can't vent its heat anywhere but back into the spacecraft, it's actually making the air inside the
ship warmer.

Instead, you'll need to use the TEST to extend the thermal radiators. Fortunately, the diagnostic program (your puzzle
input) is already equipped for this. Unfortunately, your Intcode computer is not.

Your computer is only missing a few opcodes:

Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the
second parameter. Otherwise, it does nothing.

Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second
parameter. Otherwise, it does nothing.

Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by
the third parameter. Otherwise, it stores 0.

Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the
third parameter. Otherwise, it stores 0.

Like all instructions, these instructions need to support parameter modes as described above.

Normally, after an instruction is finished, the instruction pointer increases by the number of values in that
instruction. However, if the instruction modifies the instruction pointer, that value is used and the instruction
pointer is not automatically increased.

For example, here are several programs that take one input, compare it to the value 8, and then produce one output:

3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if
it is not).

3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if
it is not).

3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it
is not).

3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if
it is not).

Here are some jump tests that take an input, then output 0 if the input was zero or 1 if the input was non-zero:

3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)
Here's a larger example:

3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99

The above example program uses an input instruction to ask for a single number. The program will then output 999 if the
input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than
8.

This time, when the TEST diagnostic program runs its input instruction to get the ID of the system to test, provide it
5, the ID for the ship's thermal radiator controller. This diagnostic test suite only outputs one number, the diagnostic
code.

What is the diagnostic code for system ID 5?

Your puzzle answer was 9217546.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable


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


def part1(current_puzzle):
    io = IO(1)
    run_program(current_puzzle, io)
    return io.output[-1]


def part2(current_puzzle):
    io = IO(5)
    run_program(current_puzzle, io)
    return io.output[-1]


if __name__ == "__main__":
    with open("_05_sunny_with_a_chance_of_asteroids.txt") as file:
        puzzle = [int(n) for n in "\n".join(file.readlines()).split(",")]
        print("part 1:", part1(list(puzzle)))
        print("part 2:", part2(list(puzzle)))
