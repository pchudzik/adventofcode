import pytest

from _07_amplification_circuit import find_max_thruster_signal, run_program, IO

sample1 = (3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0)
sample2 = (3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0)
sample3 = (
    3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31,
    31, 4, 31, 99, 0, 0, 0
)


@pytest.mark.parametrize(
    "initial_state, final_state", [
        ((1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50), (3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50)),
        ((1, 0, 0, 0, 99), (2, 0, 0, 0, 99)),
        ((2, 3, 0, 3, 99), (2, 3, 0, 6, 99)),
        ((2, 4, 4, 5, 99, 0), (2, 4, 4, 5, 99, 9801)),
        ((1, 1, 1, 4, 99, 5, 6, 0, 99), (30, 1, 1, 4, 2, 5, 6, 0, 99))
    ]
)
def test_run_program(initial_state, final_state):
    result = run_program(list(initial_state))
    assert tuple(result) == final_state


def test_with_immediate_mode():
    result = run_program([1002, 4, 3, 4, 33])

    assert tuple(result) == (1002, 4, 3, 4, 99)


def test_with_io():
    io = IO(13)
    result = run_program([3, 0, 4, 0, 99], io)

    assert io.output == [13]
    assert result == [13, 0, 4, 0, 99]


@pytest.mark.parametrize(
    "io_input, expected_output", [
        (8, 1),
        (7, 0),
        (9, 0)
    ]
)
def test_equal_position_mode(io_input, expected_output):
    io = IO(io_input)

    run_program([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], io)

    assert io.output[-1] == expected_output


@pytest.mark.parametrize(
    "io_input, expected_output", [
        (8, 1),
        (7, 0),
        (9, 0)
    ]
)
def test_equal_immediate_mode(io_input, expected_output):
    io = IO(io_input)

    run_program([3, 3, 1108, -1, 8, 3, 4, 3, 99], io)

    assert io.output[-1] == expected_output


@pytest.mark.parametrize(
    "io_input, expected_output", [
        (8, 0),
        (7, 1),
        (9, 0)
    ]
)
def test_less_then_position_mode(io_input, expected_output):
    io = IO(io_input)

    run_program([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], io)

    assert io.output[-1] == expected_output


@pytest.mark.parametrize(
    "io_input, expected_output", [
        (8, 0),
        (7, 1),
        (9, 0)
    ]
)
def test_less_then_immediate_mode(io_input, expected_output):
    io = IO(io_input)

    run_program([3, 3, 1107, -1, 8, 3, 4, 3, 99], io)

    assert io.output[-1] == expected_output


@pytest.mark.parametrize(
    "io_input, expected_output", [
        (0, 0),
        (1, 1),
    ]
)
def test_jumps_position_mode(io_input, expected_output):
    io = IO(io_input)

    run_program([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], io)

    assert io.output[-1] == expected_output


@pytest.mark.parametrize(
    "io_input, expected_output", [
        (0, 0),
        (1, 1),
    ]
)
def test_jumps_immediate_mode(io_input, expected_output):
    io = IO(io_input)

    run_program([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], io)

    assert io.output[-1] == expected_output


@pytest.mark.parametrize(
    "io_input, expected_output", [
        (7, 999),
        (8, 1000),
        (9, 1001)
    ]
)
def test_bigger_example(io_input, expected_output):
    io = IO(io_input)

    run_program([
        3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
        1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
        999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
    ], io)

    assert io.output[-1] == expected_output


@pytest.mark.parametrize(
    "puzzle, max_thrust", [
        (sample1, 43210),
        (sample2, 54321),
        (sample3, 65210)
    ]
)
def test_find_max_thruster_signal(puzzle, max_thrust):
    assert find_max_thruster_signal(puzzle) == max_thrust
