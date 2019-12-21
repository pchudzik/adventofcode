"""
--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b
stands in position 1, and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3
on abcde produces cdeab).

Exchange, written xA/B, makes the programs at positions A and B swap places.

Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do the following dance:

s1, a spin of size 1: eabcd.
x3/4, swapping the last two programs: eabdc.
pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs
standing after their dance?

Your puzzle answer was kpfonjglcibaedhm.

--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including the
first dance, a total of one billion (1000000000) times.

In the example above, their second dance would begin with the order baedc, and use the same dance moves:

s1, a spin of size 1: cbaed.
x3/4, swapping the last two programs: cbade.
pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?

Your puzzle answer was odiabmplhfgjcekn.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


def dance(program, cmds):
    for cmd in cmds:
        program = cmd(program)
    return program


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
        return "".join(program)

    return action


def spin(number):
    def action(program):
        if number == 0:
            return program
        return program[-number:] + program[:len(program) - number]

    return action


def _find_cycle(program, cmds):
    states = dict()
    cycle = [program]

    while True:
        output = dance(program, cmds)
        if output in states:
            break
        states[program] = output
        cycle.append(output)
        program = output

    return cycle


def dance_many(program, cmds, x):
    cycle = _find_cycle(program, cmds)
    last_loop_break_index = x % len(cycle)
    return cycle[last_loop_break_index]


if __name__ == "__main__":
    with open("16_permutation_promenade.txt") as file:
        cmds = [parse_cmd(cmd) for cmd in file.read().split(",")]
        program = "abcdefghijklmnop"

        print(f"part 1: {dance(program, cmds)}")
        print(f"part 2: {dance_many(program, cmds, 1_000_000_000)}")
