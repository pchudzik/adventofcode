import pytest

from _11_transporter import is_valid, find_moves, get_hash, move


@pytest.mark.parametrize(
    "state, expected", [
        ([1, 2], True),
        ([-1, -2], True),
        ([1, -1], True),
        ([1, -1, 2], False),
        ([1, -1, -2], True),
        ([1, -1, -2, 2], True),
        ([-1, 2], False),
        ([-1, -2, 2, 3], False),
        ([-1, -2, 2, -3, 3], True),
        ([-1, 1, -2, 2], True)
    ])
def test_is_valid(state, expected):
    assert is_valid(state) == expected


@pytest.mark.parametrize(
    "elevator, state, expected", [
        (0, [{1, 2}, {-1}, {-2}, {}], "020111100"),
        (3, [{}, {}, {}, {1, -1, 2, -2}], "300000042")
    ])
def test_get_hash(elevator, state, expected):
    assert get_hash(elevator, state) == expected


def test_move():
    state = [
        [1, 2],
        [-1],
        [-2],
        []
    ]

    move(0, state, 1, 0, 1)

    assert state == [
        [2],
        [-1, 1],
        [-2],
        []
    ]

    state = [
        [2],
        [-1, 1],
        [-2],
        []
    ]

    move(1, state, 1, 0, 1)

    assert state == [
        [2],
        [1],
        [-2, -1],
        []
    ]

    state = [
        [2],
        [1],
        [-2, -1],
        []
    ]

    move(1, state, 1, 0, 1)

    assert state == [
        [2],
        [],
        [-2, 1, -1],
        []
    ]


def test_find_moves():
    """
    F4 .  .  .  .  .
    F3 .  .  .  LG .
    F2 .  HG .  .  .
    F1 E  .  HM .  LM
    """
    initial = [
        [1, 2],
        [-1],
        [-2],
        []
    ]
    assert find_moves(initial) == 11
