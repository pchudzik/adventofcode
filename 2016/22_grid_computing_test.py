import importlib
import pytest

module = importlib.import_module("22_grid_computing")
Node = module.Node
find_pairs_viable_to_transfer = module.find_pairs_viable_to_transfer


def test_parse_node():
    node = Node.parse("/dev/grid/node-x4-y24    90T   70T    20T   77%")

    assert node.x == 4
    assert node.y == 24
    assert node.size == 90
    assert node.used == 70
    assert node.available == 20
    assert node.usage == 0.7778


@pytest.mark.parametrize(
    "first, second, result",
    [
        ((90, 70), (120, 10), True),
        ((90, 70), (125, 20), True),
        ((90, 70), (130, 90), False)])
def test_will_fit(first, second, result):
    node1 = Node(0, 0, *first)
    node2 = Node(1, 2, *second)

    assert node1.can_transfer_to(node2) == result


def test_transfer_data_to_the_same_node():
    node1 = Node(0, 0, 100, 1)
    node2 = Node(0, 0, 100, 1)

    assert not node1.can_transfer_to(node2)
    assert not node1.can_transfer_to(node1)
    assert not node2.can_transfer_to(node1)


def test_transfer_from_empty_node():
    empty_node = Node(0, 0, 100, 0)
    other_node = Node(1, 1, 100, 1)

    assert not empty_node.can_transfer_to(other_node)


def test_find_pairs_viable_to_transfer():
    node1 = Node(0, 0, 100, 1)
    node2 = Node(1, 0, 100, 1)
    node3 = Node(4, 0, 100, 1)
    node4 = Node(5, 0, 100, 1)
    node5 = Node(6, 0, 100, 100)

    viable_to_transfer = find_pairs_viable_to_transfer([
        node1,
        node2,
        node3,
        node4,
        node5])

    assert len(viable_to_transfer) == 12

    assert (node1, node2) in viable_to_transfer
    assert (node1, node3) in viable_to_transfer
    assert (node1, node4) in viable_to_transfer

    assert (node2, node1) in viable_to_transfer
    assert (node2, node3) in viable_to_transfer
    assert (node2, node4) in viable_to_transfer

    assert (node3, node1) in viable_to_transfer
    assert (node3, node2) in viable_to_transfer
    assert (node3, node4) in viable_to_transfer

    assert (node4, node1) in viable_to_transfer
    assert (node4, node2) in viable_to_transfer
    assert (node4, node3) in viable_to_transfer


