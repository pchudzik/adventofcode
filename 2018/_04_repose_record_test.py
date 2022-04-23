from _04_repose_record import parse, find_most_lazy_guard, find_most_lazy_guard_by_minute

puzzle = [
    "[1518-11-02 00:50] wakes up",
    "[1518-11-04 00:36] falls asleep",
    "[1518-11-01 00:05] falls asleep",
    "[1518-11-03 00:24] falls asleep",
    "[1518-11-05 00:55] wakes up",
    "[1518-11-02 00:40] falls asleep",
    "[1518-11-04 00:46] wakes up",
    "[1518-11-01 00:30] falls asleep",
    "[1518-11-01 00:55] wakes up",
    "[1518-11-01 23:58] Guard #99 begins shift",
    "[1518-11-03 00:29] wakes up",
    "[1518-11-01 00:00] Guard #10 begins shift",
    "[1518-11-03 00:05] Guard #10 begins shift",
    "[1518-11-04 00:02] Guard #99 begins shift",
    "[1518-11-05 00:45] falls asleep",
    "[1518-11-01 00:25] wakes up",
    "[1518-11-05 00:03] Guard #99 begins shift",
]


def test_parse():
    guards = parse(puzzle)

    assert guards[10].id == 10
    assert guards[10].total_asleep == 50
    assert guards[10].most_sleepy_minute == (24, 2)

    assert guards[99].id == 99
    assert guards[99].total_asleep == 30
    assert guards[99].most_sleepy_minute == (45, 3)


def test_find_lazy_guard():
    guards = parse(puzzle)

    assert find_most_lazy_guard(guards.values()).id == 10


def test_find_most_lazy_guard_by_minute():
    guards = parse(puzzle)

    assert find_most_lazy_guard_by_minute(guards.values()).id == 99
