import pytest

from _06_memory_reallocation import run_redistribution, find_cycle


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

    all_seen_states, cycling_state = find_cycle(input_state)

    assert cycling_state == (2, 4, 1, 2)
    assert all_seen_states == {
        (0, 2, 7, 0),
        (2, 4, 1, 2),
        (3, 1, 2, 3),
        (0, 2, 3, 4),
        (1, 3, 4, 1)
    }
