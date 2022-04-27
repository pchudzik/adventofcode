"""
--- Day 7: Amplification Circuit ---

Based on the navigational maps, you're going to need to send more power to your ship's thrusters to reach Santa in time.
To do this, you'll need to configure a series of amplifiers already installed on the ship.

There are five amplifiers connected in series; each one receives an input signal and produces an output signal. They are
connected such that the first amplifier's output leads to the second amplifier's input, the second amplifier's output
leads to the third amplifier's input, and so on. The first amplifier's input value is 0, and the last amplifier's output
leads to your ship's thrusters.

    O-------O  O-------O  O-------O  O-------O  O-------O
0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
    O-------O  O-------O  O-------O  O-------O  O-------O

The Elves have sent you some Amplifier Controller Software (your puzzle input), a program that should run on your
existing Intcode computer. Each amplifier will need to run a copy of the program.

When a copy of the program starts running on an amplifier, it will first use an input instruction to ask the amplifier
for its current phase setting (an integer from 0 to 4). Each phase setting is used exactly once, but the Elves can't
remember which amplifier needs which phase setting.

The program will then call another input instruction to get the amplifier's input signal, compute the correct output
signal, and supply it back to the amplifier with an output instruction. (If the amplifier has not yet received an input
signal, it waits until one arrives.)

Your job is to find the largest output signal that can be sent to the thrusters by trying every possible combination of
phase settings on the amplifiers. Make sure that memory is not shared or reused between copies of the program.

For example, suppose you want to try the phase setting sequence 3,1,2,4,0, which would mean setting amplifier A to phase
setting 3, amplifier B to setting 1, C to 2, D to 4, and E to 0. Then, you could determine the output signal that gets
sent from amplifier E to the thrusters with the following steps:

Start the copy of the amplifier controller software that will run on amplifier A. At its first input instruction,
provide it the amplifier's phase setting, 3. At its second input instruction, provide it the input signal, 0. After some
calculations, it will use an output instruction to indicate the amplifier's output signal.

Start the software for amplifier B. Provide it the phase setting (1) and then whatever output signal was produced from
amplifier A. It will then produce a new output signal destined for amplifier C.

Start the software for amplifier C, provide the phase setting (2) and the value from amplifier B, then collect its
output signal.

Run amplifier D's software, provide the phase setting (4) and input value, and collect its output signal.

Run amplifier E's software, provide the phase setting (0) and input value, and collect its output signal.

The final output signal from amplifier E would be sent to the thrusters. However, this phase setting sequence may not
have been the best one; another sequence might have sent a higher signal to the thrusters.

Here are some example programs:

Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0

Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):
3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0

Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):
3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0

Try every combination of phase settings on the amplifiers. What is the highest signal that can be sent to the thrusters?

Your puzzle answer was 101490.

--- Part Two ---

It's no good - in this configuration, the amplifiers can't generate a large enough output signal to produce the thrust
you'll need. The Elves quickly talk you through rewiring the amplifiers into a feedback loop:

      O-------O  O-------O  O-------O  O-------O  O-------O
0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
   |  O-------O  O-------O  O-------O  O-------O  O-------O |
   |                                                        |
   '--------------------------------------------------------+
                                                            |
                                                            v
                                                     (to thrusters)

Most of the amplifiers are connected as they were before; amplifier A's output is connected to amplifier B's input, and
so on. However, the output from amplifier E is now connected into amplifier A's input. This creates the feedback loop:
the signal will be sent through the amplifiers many times.

In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9, again each used
exactly once. These settings will cause the Amplifier Controller Software to repeatedly take input and produce output
many times before halting. Provide each amplifier its phase setting at its first input instruction; all further
input/output instructions are for signals.

Don't restart the Amplifier Controller Software on any amplifier during this process. Each one should continue receiving
and sending signals until it halts.

All signals sent or received in this process will be between pairs of amplifiers except the very first signal and the
very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once.

Eventually, the software on the amplifiers will halt after they have processed the final loop. When this happens, the
last output signal from amplifier E is sent to the thrusters. Your job is to find the largest output signal that can be
sent to the thrusters using the new phase settings and feedback loop arrangement.

Here are some example programs:

Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10

Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that can be
sent to the thrusters?

Your puzzle answer was 61019896.

Both parts of this puzzle are complete! They provide two gold stars: **
"""
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


class ChainedAmplifiers:
    def __init__(self, program: tuple[int], sequence: Sequence[int]):
        self.program = program
        self.thruster = self.Thruster()

        a = self.Amplifier([sequence[0], 0])
        b = self.Amplifier([sequence[1]])
        c = self.Amplifier([sequence[2]])
        d = self.Amplifier([sequence[3]])
        e = self.Amplifier([sequence[4]])

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

    class Thruster:
        def __init__(self):
            self.value = None

        def add_input(self, value):
            self.value = value

        def set_output(self, value):
            self.value = value

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


class AmplificationCircuit:
    def __init__(self, program: tuple[int, ...], sequence: Sequence[int]):
        self.program = program

        a = self.Amplifier([sequence[0], 0])
        b = self.Amplifier([sequence[1]])
        c = self.Amplifier([sequence[2]])
        d = self.Amplifier([sequence[3]])
        e = self.Amplifier([sequence[4]])

        a.next_amplifier = b
        b.next_amplifier = c
        c.next_amplifier = d
        d.next_amplifier = e
        e.next_amplifier = a

        self.amplifiers = [a, b, c, d, e]

    def execute(self):
        cpus = [Computer(amp, list(self.program)) for amp in self.amplifiers]
        current_cpu = 0
        while any(not c.is_halted for c in cpus):
            cpu = cpus[current_cpu]
            try:
                cpu.execute()
            except NoInputAvailable as e:
                pass
            current_cpu += 1
            if current_cpu >= len(cpus):
                current_cpu = 0

        return self.amplifiers[0].initial_input[-1]

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


class NoInputAvailable(Exception):
    def __init__(self, cpu):
        self.cpu = cpu


class Computer:
    def __init__(self, io: IO, puzzle: list[int], pointer: int = 0):
        self.program = puzzle
        self.pointer = pointer
        self.io = io
        self.is_halted = False

    def execute_step(self):
        try:
            cmd = self.__get_command()
            cmd.execute()
        except IndexError:
            raise NoInputAvailable(self)

    def execute(self):
        try:
            while not self.is_halted:
                self.execute_step()
        except StopIteration:
            self.is_halted = True
            return self

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

    def move(self, move_offset: int):
        self.pointer += move_offset

    def jump_to(self, pointer):
        self.pointer = pointer

    def _set_result(self, result: int, result_position: int, move_offset: int):
        position = self.pointer + result_position
        result_index = self.program[position]
        updated_program = list(self.program[:])
        updated_program[result_index] = result
        updated_pointer = self.pointer + move_offset
        self.pointer = updated_pointer
        self.program = updated_program

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
        thrust = ChainedAmplifiers(program, input_sequence).execute()
        max_thrust = max(thrust, max_thrust)

    return max_thrust


def find_max_thrust_amplified(program):
    max_thrust = -1
    for input_sequence in itertools.permutations((5, 6, 7, 8, 9)):
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
    print("part 2:", find_max_thrust_amplified(puzzle))
