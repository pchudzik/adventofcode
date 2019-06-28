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

    assert maze.shortest_path((3,1)) == 4
    assert maze.shortest_path((4,2)) == 4
    assert maze.shortest_path((4,1)) == 5
    assert maze.shortest_path((7,4)) == 11
