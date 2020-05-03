import importlib
import pytest

module = importlib.import_module("15_beverage_bandits")

parse = module.parse
sort_by_reading_order = module.sort_by_reading_order
play_game1 = module.play_game1
play_game2 = module.play_game2
Unit = module.Unit


def test_parse():
    expected_walls = {
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
        (6, 1), (6, 2), (6, 3), (6, 4),
        (5, 4), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4),
        (0, 3), (0, 2), (0, 1)
    }

    expected_elves = {
        (4, 1),
        (1, 2), (5, 2),
        (4, 3)
    }

    expected_goblins = {
        (2, 1),
        (3, 2),
        (2, 3)
    }

    puzzle = [
        "#######",
        "#.G.E.#",
        "#E.G.E#",
        "#.G.E.#",
        "#######"
    ]

    board = parse(puzzle)

    assert len(expected_walls) == len(board.walls)
    assert expected_walls == set(board.walls)

    assert len(expected_elves) == len(board.elves)
    assert expected_elves == {e.position for e in board.elves}

    assert len(expected_goblins) == len(board.goblins)
    assert expected_goblins == {g.position for g in board.goblins}


def test_move_order():
    board = parse([
        "#######",
        "#.G.E.#",
        "#E.G.E#",
        "#.G.E.#",
        "#######"
    ])

    units_move_order = [u.position for u in sorted(board.units, key=sort_by_reading_order)]
    assert units_move_order == [
        (2, 1), (4, 1),
        (1, 2), (3, 2), (5, 2),
        (2, 3), (4, 3)
    ]


def test_sort_order():
    unit1 = Unit("G", (13, 8), 3)
    unit2 = Unit("G", (11, 9), 3)
    unit3 = Unit("G", (23, 11), 3)
    unit4 = Unit("G", (12, 12), 3)
    unit5 = Unit("G", (22, 12), 3)
    unit6 = Unit("E", (23, 12), 3)
    unit7 = Unit("G", (11, 13), 3)
    unit8 = Unit("G", (21, 13), 3)
    all_units = [unit8, unit7, unit6, unit5, unit4, unit3, unit2, unit1]

    assert sorted(all_units, key=sort_by_reading_order) == [unit1, unit2, unit3, unit4, unit5, unit6, unit7, unit8]


def test_move():
    board = parse([
        "#########",
        "#G..G..G#",
        "#.......#",
        "#.......#",
        "#G..E..G#",
        "#.......#",
        "#.......#",
        "#G..G..G#",
        "#########"
    ])

    board.tick()

    assert board.elves[0].position == (4, 3)

    assert board.goblins[0].position == (2, 1)
    assert board.goblins[1].position == (6, 1)
    assert board.goblins[2].position == (4, 2)
    assert board.goblins[3].position == (7, 3)
    assert board.goblins[4].position == (2, 4)
    assert board.goblins[5].position == (1, 6)
    assert board.goblins[6].position == (4, 6)
    assert board.goblins[7].position == (7, 6)

    board.tick()

    assert board.elves[0].position == (4, 3)

    assert board.goblins[0].position == (3, 1)
    assert board.goblins[1].position == (5, 1)
    assert board.goblins[2].position == (4, 2)
    assert board.goblins[3].position == (2, 3)
    assert board.goblins[4].position == (6, 3)
    assert board.goblins[5].position == (1, 5)
    assert board.goblins[6].position == (4, 5)
    assert board.goblins[7].position == (7, 5)

    board.tick()

    assert board.elves[0].position == (4, 3)

    assert board.goblins[0].position == (3, 2)
    assert board.goblins[1].position == (4, 2)
    assert board.goblins[2].position == (5, 2)
    assert board.goblins[3].position == (3, 3)
    assert board.goblins[4].position == (5, 3)
    assert board.goblins[5].position == (1, 4)
    assert board.goblins[6].position == (4, 4)
    assert board.goblins[7].position == (7, 5)


def test_move_reading_order_1():
    board = parse([
        "#######",
        "#.E...#",
        "#.....#",
        "#...G.#",
        "#######",
    ])

    board.elves[0].do_turn(board)

    assert board.elves[0].position == (3, 1)


def test_move_reading_order_2():
    board = parse([
        "#########",
        "#......G#",
        "#G.G...E#",
        "#########"
    ])

    board.tick()

    assert board.elves[0].position == (7, 2)
    assert board.goblins[0].position == (1, 1)
    assert board.goblins[1].position == (7, 1)
    assert board.goblins[2].position == (4, 2)


def test_move_reading_order_3():
    board = parse([
        "#######",
        "#######",
        "#.E..G#",
        "#.#####",
        "#G#####",
        "#######",
        "#######",
    ])

    board.tick()

    assert board.elves[0].position == (3, 2)


def test_attack_order():
    board = parse([
        "####",
        "#GG#",
        "#.E#",
        "####",
    ])

    board.tick()

    assert board.goblins[0].position == (2, 1)
    assert board.goblins[0].hp == 197
    assert board.goblins[1].position == (1, 2)
    assert board.goblins[1].hp == 200
    assert board.elves[0].position == (2, 2)
    assert board.elves[0].hp == 194


def test_attack():
    board = parse([
        "#######",
        "#.G...#",
        "#...EG#",
        "#.#.#G#",
        "#..G#E#",
        "#.....#",
        "#######",
    ])

    board.tick()

    assert len(board.elves) == 2
    assert board.elves[0].position == (4, 2)
    assert board.elves[0].hp == 197
    assert board.elves[1].position == (5, 4)
    assert board.elves[1].hp == 197

    assert len(board.goblins) == 4
    assert board.goblins[0].position == (3, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (5, 2)
    assert board.goblins[1].hp == 197
    assert board.goblins[2].position == (3, 3)
    assert board.goblins[2].hp == 200
    assert board.goblins[3].position == (5, 3)
    assert board.goblins[3].hp == 197

    board.tick()

    assert len(board.elves) == 2
    assert board.elves[0].position == (4, 2)
    assert board.elves[0].hp == 188
    assert board.elves[1].position == (5, 4)
    assert board.elves[1].hp == 194

    assert len(board.goblins) == 4
    assert board.goblins[0].position == (4, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (3, 2)
    assert board.goblins[1].hp == 200
    assert board.goblins[2].position == (5, 2)
    assert board.goblins[2].hp == 194
    assert board.goblins[3].position == (5, 3)
    assert board.goblins[3].hp == 194

    for i in range(2, 23):
        board.tick()

    assert len(board.elves) == 1
    assert board.elves[0].position == (5, 4)
    assert board.elves[0].hp == 131

    assert len(board.goblins) == 4
    assert board.goblins[0].position == (4, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (3, 2)
    assert board.goblins[1].hp == 200
    assert board.goblins[2].position == (5, 2)
    assert board.goblins[2].hp == 131
    assert board.goblins[3].position == (5, 3)
    assert board.goblins[3].hp == 131

    board.tick()  # 24

    assert len(board.elves) == 1
    assert board.elves[0].position == (5, 4)
    assert board.elves[0].hp == 128

    assert len(board.goblins) == 4
    assert board.goblins[0].position == (3, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (4, 2)
    assert board.goblins[1].hp == 131
    assert board.goblins[2].position == (3, 3)
    assert board.goblins[2].hp == 200
    assert board.goblins[3].position == (5, 3)
    assert board.goblins[3].hp == 128

    board.tick()  # 25

    assert len(board.elves) == 1
    assert board.elves[0].position == (5, 4)
    assert board.elves[0].hp == 125

    assert len(board.goblins) == 4
    assert board.goblins[0].position == (2, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (3, 2)
    assert board.goblins[1].hp == 131
    assert board.goblins[2].position == (5, 3)
    assert board.goblins[2].hp == 125
    assert board.goblins[3].position == (3, 4)
    assert board.goblins[3].hp == 200

    board.tick()  # 26

    assert len(board.elves) == 1
    assert board.elves[0].position == (5, 4)
    assert board.elves[0].hp == 122

    assert len(board.goblins) == 4
    assert board.goblins[0].position == (1, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (2, 2)
    assert board.goblins[1].hp == 131
    assert board.goblins[2].position == (5, 3)
    assert board.goblins[2].hp == 122
    assert board.goblins[3].position == (3, 5)
    assert board.goblins[3].hp == 200

    board.tick()  # 27

    assert len(board.elves) == 1
    assert board.elves[0].position == (5, 4)
    assert board.elves[0].hp == 119

    assert len(board.goblins) == 4
    assert board.goblins[0].position == (1, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (2, 2)
    assert board.goblins[1].hp == 131
    assert board.goblins[2].position == (5, 3)
    assert board.goblins[2].hp == 119
    assert board.goblins[3].position == (4, 5)
    assert board.goblins[3].hp == 200

    board.tick()  # 28

    assert len(board.elves) == 1
    assert board.elves[0].position == (5, 4)
    assert board.elves[0].hp == 113

    assert board.goblins[0].position == (1, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (2, 2)
    assert board.goblins[1].hp == 131
    assert board.goblins[2].position == (5, 3)
    assert board.goblins[2].hp == 116
    assert board.goblins[3].position == (5, 5)
    assert board.goblins[3].hp == 200

    for i in range(28, 47):
        board.tick()

    assert len(board.elves) == 0

    assert len(board.goblins) == 4
    assert board.goblins[0].position == (1, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (2, 2)
    assert board.goblins[1].hp == 131
    assert board.goblins[2].position == (5, 3)
    assert board.goblins[2].hp == 59
    assert board.goblins[3].position == (5, 5)
    assert board.goblins[3].hp == 200

    with pytest.raises(StopIteration):
        board.tick()

    assert board.remaining_hit_points == 590
    assert board.rounds == 47


def test_attack_auto_0():
    board = parse([
        "#######",
        "#.G...#",
        "#...EG#",
        "#.#.#G#",
        "#..G#E#",
        "#.....#",
        "#######",
    ])

    assert play_game1(board) == 27730

    assert board.rounds == 47
    assert board.remaining_hit_points == 590

    assert len(board.elves) == 0
    assert len(board.goblins) == 4
    assert board.goblins[0].position == (1, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (2, 2)
    assert board.goblins[1].hp == 131
    assert board.goblins[2].position == (5, 3)
    assert board.goblins[2].hp == 59
    assert board.goblins[3].position == (5, 5)
    assert board.goblins[3].hp == 200


def test_attack_auto_1():
    board = parse([
        "#######",
        "#G..#E#",
        "#E#E.E#",
        "#G.##.#",
        "#...#E#",
        "#...E.#",
        "#######",
    ])

    assert play_game1(board) == 36334
    assert board.rounds == 37
    assert board.remaining_hit_points == 982

    assert len(board.goblins) == 0
    assert len(board.elves) == 5
    assert board.elves[0].position == (5, 1)
    assert board.elves[0].hp == 200
    assert board.elves[1].position == (1, 2)
    assert board.elves[1].hp == 197
    assert board.elves[2].position == (2, 3)
    assert board.elves[2].hp == 185
    assert board.elves[3].position == (1, 4)
    assert board.elves[3].hp == 200
    assert board.elves[4].position == (5, 4)
    assert board.elves[4].hp == 200


def test_attack_auto_2():
    board = parse([
        "#######",
        "#E..EG#",
        "#.#G.E#",
        "#E.##E#",
        "#G..#.#",
        "#..E#.#",
        "#######",
    ])

    assert play_game1(board) == 39514
    assert board.rounds == 46
    assert board.remaining_hit_points == 859

    assert len(board.goblins) == 0
    assert len(board.elves) == 5
    assert board.elves[0].position == (2, 1)
    assert board.elves[0].hp == 164
    assert board.elves[1].position == (4, 1)
    assert board.elves[1].hp == 197
    assert board.elves[2].position == (3, 2)
    assert board.elves[2].hp == 200
    assert board.elves[3].position == (1, 3)
    assert board.elves[3].hp == 98
    assert board.elves[4].position == (2, 4)
    assert board.elves[4].hp == 200


def test_attack_auto_3():
    board = parse([
        "#######",
        "#E.G#.#",
        "#.#G..#",
        "#G.#.G#",
        "#G..#.#",
        "#...E.#",
        "#######",
    ])

    assert play_game1(board) == 27755
    assert board.rounds == 35
    assert board.remaining_hit_points == 793

    assert len(board.elves) == 0
    assert len(board.goblins) == 5
    assert board.goblins[0].position == (1, 1)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (3, 1)
    assert board.goblins[1].hp == 98
    assert board.goblins[2].position == (3, 2)
    assert board.goblins[2].hp == 200
    assert board.goblins[3].position == (5, 4)
    assert board.goblins[3].hp == 95
    assert board.goblins[4].position == (4, 5)
    assert board.goblins[4].hp == 200


def test_attack_auto_4():
    board = parse([
        "#######",
        "#.E...#",
        "#.#..G#",
        "#.###.#",
        "#E#G#G#",
        "#...#G#",
        "#######",
    ])

    assert play_game1(board) == 28944
    assert board.rounds == 54
    assert board.remaining_hit_points == 536

    assert len(board.elves) == 0
    assert len(board.goblins) == 4
    assert board.goblins[0].position == (3, 2)
    assert board.goblins[0].hp == 200
    assert board.goblins[1].position == (1, 5)
    assert board.goblins[1].hp == 98
    assert board.goblins[2].position == (3, 5)
    assert board.goblins[2].hp == 38
    assert board.goblins[3].position == (5, 5)
    assert board.goblins[3].hp == 200


def test_attack_auto_5():
    board = parse([
        "#########",
        "#G......#",
        "#.E.#...#",
        "#..##..G#",
        "#...##..#",
        "#...#...#",
        "#.G...G.#",
        "#.....G.#",
        "#########",
    ])

    assert play_game1(board) == 18740
    assert board.rounds == 20
    assert board.remaining_hit_points == 937

    assert len(board.elves) == 0
    assert len(board.goblins) == 5
    assert board.goblins[0].position == (2, 1)
    assert board.goblins[0].hp == 137
    assert board.goblins[1].position == (1, 2)
    assert board.goblins[1].hp == 200
    assert board.goblins[2].position == (3, 2)
    assert board.goblins[2].hp == 200
    assert board.goblins[3].position == (2, 3)
    assert board.goblins[3].hp == 200
    assert board.goblins[4].position == (2, 5)
    assert board.goblins[4].hp == 200


def test_attack_force_elves_win_1():
    puzzle = [
        "#######",
        "#.G...#",
        "#...EG#",
        "#.#.#G#",
        "#..G#E#",
        "#.....#",
        "#######",
    ]

    assert play_game2(puzzle) == 4988


def test_attack_force_elves_win_2():
    puzzle = [
        "#######",
        "#E..EG#",
        "#.#G.E#",
        "#E.##E#",
        "#G..#.#",
        "#..E#.#",
        "#######",
    ]

    assert play_game2(puzzle) == 31284


def test_attack_force_elves_win_3():
    puzzle = [
        "#######",
        "#E.G#.#",
        "#.#G..#",
        "#G.#.G#",
        "#G..#.#",
        "#...E.#",
        "#######",
    ]

    assert play_game2(puzzle) == 3478


def test_attack_force_elves_win_4():
    puzzle = [
        "#######",
        "#.E...#",
        "#.#..G#",
        "#.###.#",
        "#E#G#G#",
        "#...#G#",
        "#######",
    ]

    assert play_game2(puzzle) == 6474


def test_attack_force_elves_win_5():
    puzzle = [
        "#########",
        "#G......#",
        "#.E.#...#",
        "#..##..G#",
        "#...##..#",
        "#...#...#",
        "#.G...G.#",
        "#.....G.#",
        "#########",
    ]

    assert play_game2(puzzle) == 1140
