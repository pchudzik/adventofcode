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
    with open("23_registers.txt") as file:
        instructions = parse_operations([l.strip() for l in file.readlines()])
        program1 = Program()
        program2 = Program(a=1)

        program1.process(instructions)
        program2.process(instructions)

        print("part1 b value is ", program1.b)
        print("part2 b value is ", program2.b)
