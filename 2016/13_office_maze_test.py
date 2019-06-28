import importlib

Maze = importlib.import_module("13_office_maze").Maze


def test_maze():
    maze = Maze((10, 7), 10)

    assert str(maze) == "\n".join([
        ".#.####.##",
        "..#..#...#",
        "#....##...",
        "###.#.###.",
        ".##..#..#.",
        "..##....#.",
        "#...##.###"
    ])


def test_shortest_path():
    maze = Maze((10, 7), 10)

    assert maze.shortest_path((3, 1)) == 4
    assert maze.shortest_path((4, 2)) == 4
    assert maze.shortest_path((4, 1)) == 5
    assert maze.shortest_path((7, 4)) == 11


def test_all_reachable_locations_within_distance():
    maze = Maze((10, 7), 10)

    assert maze.all_reachable_locations_within_distance(10)
    assert maze.all_reachable_locations_within_distance(10) == {
        (6, 4),
        (3, 2),
        (0, 0),
        (4, 1),
        (6, 6),
        (4, 5),
        (7, 5),
        (4, 2),
        (6, 5),
        (0, 1),
        (1, 2),
        (3, 3),
        (5, 5),
        (3, 1),
        (4, 4),
        (2, 2),
        (3, 4),
        (1, 1)
    }
