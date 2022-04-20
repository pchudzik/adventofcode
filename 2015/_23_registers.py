"""
--- Day 23: Opening the Turing Lock ---

Little Jane Marie just got her very first computer for Christmas from some unknown benefactor. It comes with
instructions and an example program, but the computer itself seems to be malfunctioning. She's curious what the program
does, and would like you to help her run it.

The manual explains that the computer supports two registers and six instructions (truly, it goes on to remind the
reader, a state-of-the-art technology). The registers are named a and b, can hold any non-negative integer, and begin
with a value of 0. The instructions are as follows:

hlf r sets register r to half its current value, then continues with the next instruction.
tpl r sets register r to triple its current value, then continues with the next instruction.
inc r increments register r, adding 1 to it, then continues with the next instruction.
jmp offset is a jump; it continues with the instruction offset away relative to itself.
jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).

All three jump instructions work with an offset relative to that instruction. The offset is always written with a prefix
+ or - to indicate the direction of the jump (forward or backward, respectively). For example, jmp +1 would simply
continue with the next instruction, while jmp +0 would continuously jump back to itself forever.

The program exits when it tries to run an instruction beyond the ones defined.

For example, this program sets a to 2, because the jio instruction causes it to skip the tpl instruction:

inc a
jio a, +2
tpl a
inc a
What is the value in register b when the program in your puzzle input is finished executing?

Your puzzle answer was 170.

--- Part Two ---

The unknown benefactor is very thankful for releasi-- er, helping little Jane Marie with her computer. Definitely not to
distract you, what is the value in register b after the program is finished executing if register a starts as 1 instead?

Your puzzle answer was 247.


"""


def hlf(register):
    def do_exec(program):
        program[register] = int(program[register] / 2)
        program.next()

    return do_exec


def tpl(register):
    def do_exec(program):
        program[register] = program[register] * 3
        program.next()

    return do_exec


def inc(register):
    def do_exec(program):
        program[register] = program[register] + 1
        program.next()

    return do_exec


def jmp(number):
    def do_exec(program):
        program.jump(number)

    return do_exec


def jie(register, offset):
    def do_exec(program):
        if program[register] % 2 == 0:
            program.jump(int(offset))
        else:
            program.next()

    return do_exec


def jio(register, offset):
    def do_exec(program):
        if program[register] == 1:
            program.jump(int(offset))
        else:
            program.next()

    return do_exec


class Program:
    def __init__(self, a=0, b=0, offset=0):
        self.a = a
        self.b = b
        self.offset = offset

    def process(self, instructions):
        while self.offset < len(instructions):
            instructions[self.offset](self)

    def next(self):
        self.jump(1)

    def jump(self, offset):
        self.offset += offset

    def __getitem__(self, register):
        if register == "a":
            return self.a
        elif register == "b":
            return self.b

    def __setitem__(self, register, value):
        if register == "a":
            self.a = value
        elif register == "b":
            self.b = value


def parse_operations(operations):
    result = []

    for operation in operations:
        if operation.startswith("hlf"):
            result.append(hlf(operation.replace("hlf ", "")))
        elif operation.startswith("tpl"):
            result.append(tpl(operation.replace("tpl ", "")))
        elif operation.startswith("inc"):
            result.append(inc(operation.replace("inc ", "")))
        elif operation.startswith("jmp"):
            result.append(jmp(int(operation.replace("jmp ", ""))))
        elif operation.startswith("jie"):
            operation = operation.replace("jie ", "")
            result.append(jie(*operation.split(", ")))
        elif operation.startswith("jio"):
            operation = operation.replace("jio ", "")
            result.append(jio(*operation.split(", ")))

    return result


if __name__ == "__main__":
    with open("_23_registers.txt") as file:
        instructions = parse_operations([l.strip() for l in file.readlines()])
        program1 = Program()
        program2 = Program(a=1)

        program1.process(instructions)
        program2.process(instructions)

        print("part1 b value is ", program1.b)
        print("part2 b value is ", program2.b)
