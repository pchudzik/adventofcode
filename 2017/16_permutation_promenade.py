def dance(program, cmds):
    for cmd in cmds:
        program = cmd(program)
    return tuple(program)


def parse_cmd(cmd):
    if cmd.startswith("s"):
        number = int(cmd.replace("s", ""))
        return spin(number)
    if cmd.startswith("x"):
        src, dst = cmd.replace("x", "").split("/")
        return exchange(int(src), int(dst))
    if cmd.startswith("p"):
        src_name, dst_name = cmd.replace("p", "", 1).split("/")
        return partner(src_name, dst_name)


def partner(src_name, dst_name):
    def action(program):
        src, dst = program.index(src_name), program.index(dst_name)
        return exchange(src, dst)(program)

    return action


def exchange(src, dst):
    def action(program):
        program = [*program]
        a, b = program[src], program[dst]
        program[src] = b
        program[dst] = a
        return program

    return action


def spin(number):
    def action(program):
        if number == 0:
            return program
        return program[-number:] + program[:len(program) - number]

    return action


def part2(program, cmds):
    states = dict()
    seen = list()
    program = tuple(program)

    while True:
        if program in states:
            break
        else:
            output = dance(program, cmds)
            states[program] = output
            program = output
            seen.append("".join(output))

    start_index = seen.index("".join(program))
    # cycle = states.values()
    cycle = (1_000_000_000 - len(states)) % len(states)
    return seen[cycle]



if __name__ == "__main__":
    with open("16_permutation_promenade.txt") as file:
        puzzle = file.read().split(",")
        program = tuple([*"abcdefghijklmnop"])
        states = dict()
        cmds = [parse_cmd(c) for c in puzzle]
        hit, miss = 0, 0
        # find cycle
        # x = moves until cycle
        # reszta z dzielenia y = (1_000_000_000 - x)  // x
        # rotate result y times

        print(part2(program, cmds))
        for i in range(1_000_000_000):
            if program in states:
                output = states[program]
                hit += 1
            else:
                output = dance(program, cmds)
                states[program] = output
                miss += 1

            program = output

            if i == 0:
                print(f"part1: {''.join(program)}")
            if i % 4_000_000 == 0:
                print(f"progress={i / 1_000_000_000 * 100}, hit={hit}, miss={miss}, i={i}")
        print(f"part2 {''.join(program)}")
