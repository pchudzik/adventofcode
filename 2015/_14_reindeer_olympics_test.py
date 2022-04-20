from _14_reindeer_olympics import reindeer_parser, Reindeer, find_best_leaders, find_top_travelers


def test_parse():
    puzzle = "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."

    reindeer = reindeer_parser(puzzle)

    assert reindeer.name == "Comet"
    assert reindeer.speed == 14
    assert reindeer.fly_time == 10
    assert reindeer.rest_time == 127


def test_movement():
    comet = Reindeer(name="Comet", speed=2, fly_time=2, rest_time=3)

    assert comet.traveled_distance(1) == 2
    assert comet.traveled_distance(2) == 4
    assert comet.traveled_distance(3) == 4
    assert comet.traveled_distance(4) == 4
    assert comet.traveled_distance(5) == 4
    assert comet.traveled_distance(6) == 6
    assert comet.traveled_distance(7) == 8
    assert comet.traveled_distance(8) == 8
    assert comet.traveled_distance(9) == 8
    assert comet.traveled_distance(10) == 8
    assert comet.traveled_distance(11) == 10
    assert comet.traveled_distance(12) == 12


def test_example_movement1():
    comet = Reindeer(name="Comet", speed=14, fly_time=10, rest_time=127)

    assert comet.traveled_distance(1000) == 1120


def test_example_movement2():
    dancer = Reindeer(name="Dancer", speed=16, fly_time=11, rest_time=162)

    assert dancer.traveled_distance(1000) == 1056


def test_distance_contest():
    standings = find_top_travelers(
        [
            Reindeer(name="Comet", speed=14, fly_time=10, rest_time=127),
            Reindeer(name="Dancer", speed=16, fly_time=11, rest_time=162)
        ],
        1000)

    first_place = standings[0]
    second_place = standings[1]

    assert first_place[0].name == "Comet"
    assert first_place[1] == 1120

    assert second_place[0].name == "Dancer"
    assert second_place[1] == 1056


def test_leading_contest():
    standings = find_best_leaders(
        [
            Reindeer(name="Comet", speed=14, fly_time=10, rest_time=127),
            Reindeer(name="Dancer", speed=16, fly_time=11, rest_time=162)
        ],
        1000)
    first_place = standings[0]
    second_place = standings[1]

    assert first_place[0].name == "Dancer"
    assert first_place[1] == 689

    assert second_place[0].name == "Comet"
    assert second_place[1] == 312
