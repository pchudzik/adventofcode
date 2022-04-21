import pytest

from _17_two_steps_forward import Maze


@pytest.mark.parametrize(
    "puzzle, shortest_path", [
        ("ihgpwlah", "DDRRRD"),
        ("kglvqrro", "DDUDRLRRUDRD"),
        ("ulqzkmiv", "DRURDRUDDLLDLUURRDULRLDUUDDDRR"),
        ("gdjjyniy", "DUDDRLRRRD")])
def test_find_shortest_path(puzzle, shortest_path):
    maze = Maze(puzzle)

    assert maze.find_shortest_path() == shortest_path


def test_find_shortest_path_impossible():
    maze = Maze("hijkl")

    assert maze.find_shortest_path() is None


@pytest.mark.parametrize(
    "puzzle, longest_path", [
        ("ihgpwlah", 370),
        ("kglvqrro", 492),
        ("ulqzkmiv", 830),
        ("gdjjyniy", 578)])
def test_find_longest_path(puzzle, longest_path):
    maze = Maze(puzzle)

    assert maze.find_longest_path() == longest_path
