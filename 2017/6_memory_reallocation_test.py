import importlib
import pytest

module = importlib.import_module("6_memory_reallocation")
run_redistribution = module.run_redistribution
find_cycle = module.find_cycle


@pytest.mark.parametrize(
    "in_state, out_state", [
        [(0, 2, 7, 0), (2, 4, 1, 2)],
        [(2, 4, 1, 2), (3, 1, 2, 3)],
        [(3, 1, 2, 3), (0, 2, 3, 4)],
        [(0, 2, 3, 4), (1, 3, 4, 1)],
        [(1, 3, 4, 1), (2, 4, 1, 2)]
    ])
def test_run_cycle(in_state, out_state):
    assert run_redistribution(in_state) == out_state


def test_find_cycle():
    input_state = (0, 2, 7, 0)

    result = find_cycle(input_state)

    assert result == {
        (0, 2, 7, 0),
        (2, 4, 1, 2),
        (3, 1, 2, 3),
        (0, 2, 3, 4),
        (1, 3, 4, 1)
    }
