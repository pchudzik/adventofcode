import importlib

module = importlib.import_module("07_the_sum_of_its_parts")
find_steps_order = module.find_steps_order
parse_instructions = module.parse_instructions

instructions = [
    "Step C must be finished before step A can begin.",
    "Step C must be finished before step F can begin.",
    "Step A must be finished before step B can begin.",
    "Step A must be finished before step D can begin.",
    "Step B must be finished before step E can begin.",
    "Step D must be finished before step E can begin.",
    "Step F must be finished before step E can begin."
]


def test_part1():
    order = find_steps_order(instructions, base_working_time=0)

    assert order == (21, "CABDFE")


def test_part2():
    order = find_steps_order(instructions, workers_count=2, base_working_time=0)

    assert order == (15, "CABFDE")


def test_parse_instructions():
    steps = parse_instructions(instructions)

    assert steps["A"].name == "A"
    assert steps["A"].after_names == ["C"]
    assert steps["A"].before_names == ["B", "D"]

    assert steps["B"].name == "B"
    assert steps["B"].after_names == ["A"]
    assert steps["B"].before_names == ["E"]

    assert steps["C"].name == "C"
    assert steps["C"].after_names == []
    assert steps["C"].before_names == ["A", "F"]

    assert steps["D"].name == "D"
    assert steps["D"].after_names == ["A"]
    assert steps["D"].before_names == ["E"]

    assert steps["E"].name == "E"
    assert steps["E"].after_names == ["B", "D", "F"]
    assert steps["E"].before_names == []
