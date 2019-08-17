import importlib
import pytest

module = importlib.import_module("24_air_duct_spelunking")
Maze = module.Maze
find_shortest_path_to_all_points = module.find_shortest_path_to_all_points


@pytest.mark.parametrize(
    "number, coordinates",
    [
        (0, (1, 1)),
        (1, (3, 1)),
        (2, (9, 1)),
        (3, (9, 3)),
        (4, (1, 3))])
def test_find_location(number, coordinates):
    maze = Maze((
        "###########",
        "#0.1.....2#",
        "#.#######.#",
        "#4.......3#",
        "###########"))

    assert maze.find_location(number) == coordinates


@pytest.mark.parametrize(
    "start, end, distance",
    [
        (0, 4, 2),
        (4, 1, 4),
        (1, 2, 6),
        (2, 3, 2)])
def test_find_distance(start, end, distance):
    maze = Maze((
        "###########",
        "#0.1.....2#",
        "#.#######.#",
        "#4.......3#",
        "###########"))

    assert maze.find_path(start, end) == distance


def test_find_shortest_path():
    maze = Maze((
        "###########",
        "#0.1.....2#",
        "#.#######.#",
        "#4.......3#",
        "###########"))

    assert find_shortest_path_to_all_points(maze) == (14, 20)
