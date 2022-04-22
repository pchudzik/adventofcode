import pytest

from _09_stream_processing import process


@pytest.mark.parametrize(
    "puzzle", [
        "<>",
        "<random characters>",
        "<<<<>",
        "<{!>}>",
        "<!!>",
        "<!!!>>",
        "<{o\"i!a,<{i<a>"
    ])
def test_garbage(puzzle):
    result = process(puzzle)

    assert [(start, end) for _, start, end in result.garbage] == [(0, len(puzzle) - 1)]


@pytest.mark.parametrize(
    "puzzle, groups", [
        ("{}", [(1, 0, 1)]),
        ("{{{}}}", [(3, 2, 3), (2, 1, 4), (1, 0, 5)]),
        ("{{},{}}", [(2, 1, 2), (2, 4, 5), (1, 0, 6)]),
        ("{{{},{},{{}}}}", [(3, 2, 3), (3, 5, 6), (4, 9, 10), (3, 8, 11), (2, 1, 12), (1, 0, 13)]),
        ("{<{},{},{{}}>},", [(1, 0, 13)]),
        ("{<a>,<a>,<a>,<a>}", [(1, 0, 16)]),
        ("{{<a>},{<a>},{<a>},{<a>}}", [(2, 1, 5), (2, 7, 11), (2, 13, 17), (2, 19, 23), (1, 0, 24)]),
        ("{{<!>},{<!>},{<!>},{<a>}}", [(2, 1, 23), (1, 0, 24)])
    ])
def test_group_detector(puzzle, groups):
    result = process(puzzle)

    assert result.groups == groups


@pytest.mark.parametrize(
    "puzzle, score", [
        ("{}", 1),
        ("{{{}}},", 6),
        ("{{},{}}", 5),
        ("{{{},{},{{}}}}", 16),
        ("{<a>,<a>,<a>,<a>}", 1),
        ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
        ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
        ("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3)
    ])
def test_score(puzzle, score):
    result = process(puzzle)

    assert result.score == score


@pytest.mark.parametrize(
    "puzzle,removed", [
        ("<>", 0),
        ("<random characters>", 17),
        ("<<<<>", 3),
        ("<{!>}>", 2),
        ("<!!>", 0),
        ("<!!!>>", 0),
        ("<{o\"i!a,<{i<a>", 10)
    ])
def test_removed(puzzle, removed):
    result = process(puzzle)

    assert result.removed == removed
