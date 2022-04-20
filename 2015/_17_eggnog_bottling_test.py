from _17_eggnog_bottling import find_combinations, find_minimum_combinations


def test_bottling():
    combinations = find_combinations([20, 15, 10, 5, 5], 25)

    assert len(combinations) == 4
    assert (10, 15) in combinations
    assert combinations.count((5, 20)) == 2
    assert (5, 5, 15) in combinations


def test_minimum_bottling():
    combinations = find_minimum_combinations(find_combinations([20, 15, 10, 5, 5], 25))

    assert len(combinations) == 3
    assert (10, 15) in combinations
    assert combinations.count((5, 20)) == 2
