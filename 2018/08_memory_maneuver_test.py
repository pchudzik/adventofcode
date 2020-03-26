import importlib

module = importlib.import_module("08_memory_maneuver")
parse = module.parse

raw_nodes = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def test_read_nodes():
    root_node = parse(raw_nodes)

    assert root_node.metadata == (1, 1, 2)
    assert len(root_node.children) == 2

    root_child1 = root_node.children[0]
    root_child2 = root_node.children[1]

    assert root_child1.metadata == (10, 11, 12)
    assert len(root_child1.children) == 0

    assert root_child2.metadata == (2,)
    assert len(root_child2.children) == 1

    last_child = root_child2.children[0]

    assert last_child.metadata == (99,)
    assert len(last_child.children) == 0


def test_sum_metadata():
    root_node = parse(raw_nodes)

    assert root_node.sum_metadata == 138


def test_node_value():
    root_node = parse(raw_nodes)

    assert root_node.node_value == 66
