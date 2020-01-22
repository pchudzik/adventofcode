import importlib

module = importlib.import_module("22_sporifica_virus")
Grid = module.Grid
parse_input = module.parse_input
find_center = module.find_center
next_move = module.next_move
burst = module.burst
virus_carrier = module.virus_carrier

input = [
    "..#",
    "#..",
    "..."
]


def test_parse():
    infected = {
        (0, 2),
        (1, 0)
    }

    grid = parse_input(input)

    for x in range(3):
        for y in range(3):
            if (x, y) in infected:
                assert grid.is_infected(x, y)
            else:
                assert not grid.is_infected(x, y)


def test_find_center():
    assert find_center(input) == (1, 1)


def test_burst_when_clean():
    grid = Grid([])

    current, previous = burst((0, 0), (0, -1), grid)

    assert current == (-1, 0)
    assert previous == (0, 0)
    assert grid.is_infected(0, 0)


def test_burst_when_infected():
    grid = Grid([])
    grid.infect(0, 0)

    current, previous = burst((0, 0), (0, -1), grid)

    assert current == (1, 0)
    assert previous == (0, 0)
    assert not grid.is_infected(0, 0)


"""
-1, 1  | 0, 1   | 1, 1
-1, 0  | 0, 0   | 1, 0
-1, -1 | 0, -1  | 1, -1
"""


def test_next_move__current_infected_moving_right():
    grid = Grid([])

    grid.infect(0, 0)

    assert next_move(grid, (0, 0), (1, 0)) == (0, 1)


def test_next_move__current_clean_moving_right():
    grid = Grid([])

    assert next_move(grid, (0, 0), (1, 0)) == (0, -1)


def test_next_move__current_infected_moving_left():
    grid = Grid([])

    grid.infect(0, 0)

    assert next_move(grid, (0, 0), (-1, 0)) == (0, -1)


def test_next_move__current_clean_moving_left():
    grid = Grid([])

    assert next_move(grid, (0, 0), (-1, 0)) == (0, 1)


def test_next_move__current_infected_moving_up():
    grid = Grid([])

    grid.infect(0, 0)

    assert next_move(grid, (0, 0), (0, -1)) == (1, 0)


def test_next_move__current_clean_moving_up():
    grid = Grid([])

    assert next_move(grid, (0, 0), (0, -1)) == (-1, 0)


def test_next_move__current_infected_moving_down():
    grid = Grid([])

    grid.infect(0, 0)

    assert next_move(grid, (0, 0), (0, 1)) == (-1, 0)


def test_next_move__current_clean_moving_down():
    grid = Grid([])

    assert next_move(grid, (0, 0), (0, 1)) == (1, 0)


def test_virus_carrier():
    grid = Grid([(-1, 0), (1, 1)])

    virus_carrier(7, (0, 0), grid)

    assert grid.started_infection == 5

def test_virus_carrier():
    grid = Grid([(-1, 0), (1, 1)])

    virus_carrier(10000, (0, 0), grid)

    assert grid.started_infection == 5587