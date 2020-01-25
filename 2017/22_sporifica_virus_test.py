import importlib

module = importlib.import_module("22_sporifica_virus")
Grid = module.Grid
Grid2 = module.Grid2
parse_input = module.parse_input
find_center = module.find_center
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

    grid = Grid(infected=parse_input(input))

    for x in range(3):
        for y in range(3):
            if (x, y) in infected:
                assert grid.is_infected((x, y))
            else:
                assert not grid.is_infected((x, y))


def test_find_center():
    assert find_center(input) == (1, 1)


def test_burst_when_clean():
    grid = Grid()

    current, previous = burst((0, 0), (0, -1), grid)

    assert current == (-1, 0)
    assert previous == (0, 0)
    assert grid.is_infected((0, 0))


def test_burst_when_infected():
    grid = Grid(infected=[(0, 0)])

    current, previous = burst((0, 0), (0, -1), grid)

    assert current == (1, 0)
    assert previous == (0, 0)
    assert not grid.is_infected((0, 0))


def test_next_move__current_infected():
    """
    0,0 | 0,1 | 0,2
    1,0 | 1,1 | 1,2
    2,0 | 2,1,| 2,2

      N
    W   E
      S
    """

    grid = Grid(infected=[(1,1)])

    # moving west and turn right
    assert grid.next_move((1, 1), (1, 2)) == (0, 1)

    # moving east and turn right
    assert grid.next_move((1, 1), (1, 0)) == (2, 1)

    # moving north and turn right
    assert grid.next_move((1, 1), (2, 1)) == (1, 2)

    # moving south and turn right
    assert grid.next_move((1, 1), (0, 1)) == (1, 0)


def test_next_move__current_clean():
    """
    0,0 | 0,1 | 0,2
    1,0 | 1,1 | 1,2
    2,0 | 2,1,| 2,2

      N
    W   E
      S
    """

    grid = Grid()

    # moving west and turn left
    assert grid.next_move((1, 1), (1, 2)) == (2, 1)

    # moving north and turn left
    assert grid.next_move((1, 1), (2, 1)) == (1, 0)

    # moving east and turn left
    assert grid.next_move((1, 1), (1, 0)) == (0, 1)

    # moving south and turn left
    assert grid.next_move((1, 1), (0, 1)) == (1, 2)


def test_virus_carrier_7_2():
    grid = Grid(infected=[(0, 2), (1, 0)])

    virus_carrier(7, (1, 1), grid)

    assert grid.started_infection == 5


def test_virus_carrier_70_2():
    grid = Grid(infected=[(0, 2), (1, 0)])

    virus_carrier(70, (1, 1), grid)

    assert grid.started_infection == 41


def test_virus_carrier_10000_2():
    grid = Grid(infected=[(0, 2), (1, 0)])

    virus_carrier(10000, (1, 1), grid)

    assert grid.started_infection == 5587


def test_next_move__current_flagged():
    """
    0,0 | 0,1 | 0,2
    1,0 | 1,1 | 1,2
    2,0 | 2,1,| 2,2

      N
    W   E
      S
    """
    grid = Grid2(infected=[], weakened=[], flagged=[(1, 1)])

    # moving west and reverse
    assert grid.next_move((1, 1), (1, 2)) == (1, 2)

    # moving north and reverse
    assert grid.next_move((1, 1), (2, 1)) == (2, 1)

    # moving east and reverse
    assert grid.next_move((1, 1), (1, 0)) == (1, 0)

    # moving south turn left
    assert grid.next_move((1, 1), (0, 1)) == (0, 1)


def test_next_move__current_infected2():
    """
    0,0 | 0,1 | 0,2
    1,0 | 1,1 | 1,2
    2,0 | 2,1,| 2,2

      N
    W   E
      S
    """
    grid = Grid2(infected=[(1, 1)])

    # moving west and turn right
    assert grid.next_move((1, 1), (1, 2)) == (0, 1)

    # moving east and turn right
    assert grid.next_move((1, 1), (1, 0)) == (2, 1)

    # moving north and turn right
    assert grid.next_move((1, 1), (2, 1)) == (1, 2)

    # moving south and turn right
    assert grid.next_move((1, 1), (0, 1)) == (1, 0)


def test_next_move__current_clean2():
    """
    0,0 | 0,1 | 0,2
    1,0 | 1,1 | 1,2
    2,0 | 2,1,| 2,2

      N
    W   E
      S
    """

    grid = Grid2()

    # moving west and turn left
    assert grid.next_move((1, 1), (1, 2)) == (2, 1)

    # moving north and turn left
    assert grid.next_move((1, 1), (2, 1)) == (1, 0)

    # moving east and turn left
    assert grid.next_move((1, 1), (1, 0)) == (0, 1)

    # moving south and turn left
    assert grid.next_move((1, 1), (0, 1)) == (1, 2)


def test_next_move__current_weakened():
    """
    0,0 | 0,1 | 0,2
    1,0 | 1,1 | 1,2
    2,0 | 2,1,| 2,2

      N
    W   E
      S
    """
    grid = Grid2(weakened=[(1, 1)])

    # moving west and go ahead
    assert grid.next_move((1, 1), (1, 2)) == (1, 0)

    # moving north and turn left
    assert grid.next_move((1, 1), (2, 1)) == (0, 1)

    # moving east and turn left
    assert grid.next_move((1, 1), (1, 0)) == (1, 2)

    # moving south and turn left
    assert grid.next_move((1, 1), (0, 1)) == (2, 1)


def test_sample_part2_100():
    grid = Grid2(infected=[(0, 2), (1, 0)])

    virus_carrier(100, (1, 1), grid)

    assert grid.started_infection == 26


def x_test_sample_part2_10000000():
    grid = Grid2(infected=[(0, 2), (1, 0)])

    virus_carrier(10_000_000, (1, 1), grid)

    assert grid.started_infection == 2511944
