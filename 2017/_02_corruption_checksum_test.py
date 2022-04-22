from _02_corruption_checksum import checksum, solve_spreadsheet


def test_checksum():
    puzzle = [
        "5 1 9 5",
        "7 5 3",
        "2 4 6 8"
    ]

    assert checksum(puzzle) == 18


def test_solve_spreadsheet():
    puzzle = [
        "5 9 2 8",
        "9 4 7 3",
        "3 8 6 5"
    ]

    assert solve_spreadsheet(puzzle) == 9
