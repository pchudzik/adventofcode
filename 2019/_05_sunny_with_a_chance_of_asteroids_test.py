import pytest

from _05_sunny_with_a_chance_of_asteroids import run_program, IO


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
