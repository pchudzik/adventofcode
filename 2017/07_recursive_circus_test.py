import importlib

module = importlib.import_module("07_recursive_circus")
stack_parser = module.stack_parser
find_root_program = module.find_root_program
find_weight_of_children = module.find_weight_of_children
balance_tower = module.balance_tower

puzzle = [
    "pbga (66)",
    "xhth (57)",
    "ebii (61)",
    "havc (66)",
    "ktlj (57)",
    "fwft (72) -> ktlj, cntj, xhth",
    "qoyq (66)",
    "padx (45) -> pbga, havc, qoyq",
    "tknk (41) -> ugml, padx, fwft",
    "jptl (61)",
    "ugml (68) -> gyxo, ebii, jptl",
    "gyxo (61)",
    "cntj (57)"
]


def test_stack_parse():
    stack = stack_parser(puzzle)

    assert stack["ebii"].weight == 61
    assert stack["ugml"].weight == 68
    assert stack["padx"].weight == 45

    assert stack["ebii"].parent == stack["ugml"]
    assert stack["padx"].parent == stack["tknk"]

    assert {child.name for child in stack["tknk"].children} == {"ugml", "padx", "fwft"}
    assert {child.name for child in stack["fwft"].children} == {"ktlj", "cntj", "xhth"}
    assert {child.name for child in stack["havc"].children} == set()


def test_find_root_program():
    stack = stack_parser(puzzle)

    root_program = find_root_program(stack)

    assert root_program.name == "tknk"
    assert root_program.weight == 41


def test_find_weight_of_children():
    stack = stack_parser(puzzle)

    assert find_weight_of_children(stack, "ugml") == 251
    assert find_weight_of_children(stack, "padx") == 243
    assert find_weight_of_children(stack, "fwft") == 243


def test_balance_tower():
    stack = stack_parser(puzzle)

    assert balance_tower(stack) == ("ugml", 60)
