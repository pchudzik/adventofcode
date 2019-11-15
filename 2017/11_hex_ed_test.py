import pytest
import importlib

module = importlib.import_module("11_hex_ed")
shortest_path_finder = module.shortest_path_finder
next_coordinate = module.next_coordinate
find_distance = module.find_distance


@pytest.mark.parametrize(
    "path, number_of_steps", [
        ("ne,ne,ne", 3),
        ("ne,ne,sw,sw", 0),
        ("ne,ne,s,s", 2),
        ("se,sw,se,sw,sw", 3)])
def test_path_finder(path, number_of_steps):
    assert shortest_path_finder(path) == number_of_steps


@pytest.mark.parametrize(
    "current, move, next", [
        ((0, 0, 0), "n", (0, 1, -1)),
        ((0, 0, 0), "ne", (1, 0, -1)),
        ((0, 0, 0), "se", (1, -1, 0)),
        ((0, 0, 0), "s", (0, -1, 1)),
        ((0, 0, 0), "sw", (-1, 0, 1)),
        ((0, 0, 0), "nw", (-1, 1, 0)),
        ((1, -2, 1), "n", (1, -1, 0)),
        ((1, -2, 1), "ne", (2, -2, 0)),
        ((1, -2, 1), "se", (2, -3, 1)),
        ((1, -2, 1), "s", (1, -3, 2)),
        ((1, -2, 1), "sw", (0, -2, 2)),
        ((1, -2, 1), "nw", (0, -1, 1)),
    ])
def test_next_coordinate(current, move, next):
    assert next_coordinate(current, move) == next


@pytest.mark.parametrize(
    "start, end, distance", [
        ((0, 0, 0), (0, 4, -4), 4),
        ((0, 0, 0), (0, -4, 4), 4),
        ((0, 0, 0), (-4, 2, 2), 4),
        ((0, 0, 0), (4, -2, -2), 4),
        ((0, 0, 0), (2, -3, 1), 3),
        ((0, 0, 0), (1, -4, 3), 4),
        ((0, 0, 0), (-3, -1, 4), 4),
    ])
def test_find_distance(start, end, distance):
    assert find_distance(start, end) == distance
