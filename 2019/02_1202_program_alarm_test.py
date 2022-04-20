import importlib

import pytest

module = importlib.import_module("02_1202_program_alarm")
run_program = module.run_program


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
    result = run_program(initial_state)
    assert tuple(result) == final_state
