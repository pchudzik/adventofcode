import importlib

module = importlib.import_module("19_an_elephant_named_joseph")

Elve = module.Elve
run_round = module.run_round
find_elve_with_all_presents = module.find_elve_with_all_presents


def test_round():
    elves = [Elve(i + 1, 1) for i in range(5)]

    round1 = run_round(elves)

    assert round1 == [
        Elve(3, 2),
        Elve(5, 3)
    ]

    round2 = run_round(round1)

    assert round2 == [
        Elve(3, 5),
    ]

def test_round_2():
    elves = [Elve(i + 1, 1) for i in range(6)]

    round1 = run_round(elves)

    assert round1 == [
        Elve(1, 2),
        Elve(3, 2),
        Elve(5, 2)
    ]

    round2 = run_round(round1)

    assert round2 == [
        Elve(5, 6)
    ]


def test_find_elve_with_all_presents():
    winner = find_elve_with_all_presents([Elve(i + 1, 1) for i in range(5)])

    assert winner == Elve(3, 5)
