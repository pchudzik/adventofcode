import importlib

module = importlib.import_module("05_maze_of_twisty_trampolines")
count_jumps_1 = module.count_jumps_1
count_jumps_2 = module.count_jumps_2
Program = module.Program
Instruction = module.Instruction


def test_count_jumps_1():
    puzzle = [0, 3, 0, 1, -3]

    assert count_jumps_1(puzzle) == 5


def test_count_jumps_2():
    puzzle = [0, 3, 0, 1, -3]

    assert count_jumps_2(puzzle) == 10


def test_program_step_by_step():
    instructions = [Instruction(offset, lambda _: 1) for offset in (0, 3, 0, 1, -3)]
    program = Program(instructions)

    assert not program.is_done

    program.step()
    assert not program.is_done
    assert program.index == 0
    assert program.instructions[0].offset == 1

    program.step()
    assert not program.is_done
    assert program.index == 1
    assert program.instructions[0].offset == 2

    program.step()
    assert not program.is_done
    assert program.index == 4
    assert program.instructions[0].offset == 2
    assert program.instructions[1].offset == 1

    program.step()
    assert not program.is_done
    assert program.index == 1
    assert program.instructions[0].offset == 2
    assert program.instructions[1].offset == 1
    assert program.instructions[4].offset == 1

    program.step()
    assert program.is_done
    assert program.index == 5
    assert program.instructions[0].offset == 2
    assert program.instructions[1].offset == 2
    assert program.instructions[4].offset == 1
