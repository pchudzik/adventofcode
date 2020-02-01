import importlib

module = importlib.import_module("24_electromagnetic_moat")
Bridge = module.Bridge
parse = module.parse
find_available_bridges = module.find_available_bridges
find_strongest_bridge = module.find_strongest_bridge
find_longest_and_strongest_bridge = module.find_longest_and_strongest_bridge


def test_parse_bridge():
    assert parse(["0/2"]) == [Bridge(0, 2)]


def test_bridge_strength():
    assert Bridge(0, 3).strength == 3
    assert Bridge(3, 7).strength == 10
    assert Bridge(7, 4).strength == 11


def test_bridge_compatibility():
    assert Bridge(0, 1).compatible(0)
    assert Bridge(0, 1).compatible(1)

    assert not Bridge(0, 1).compatible(3)


def test_remaining_pin():
    assert Bridge(0, 2).remaining_pin(0) == 2
    assert Bridge(0, 2).remaining_pin(2) == 0
    assert Bridge(0, 2).remaining_pin(1) is None


def test_find_available_bridges():
    bridges = parse([
        "0/2",
        "2/2",
        "2/3",
        "3/4",
        "3/5",
        "0/1",
        "10/1",
        "9/10"])

    all_bridges = find_available_bridges(bridges)

    assert all_bridges == {
        tuple([Bridge(0, 1)]),
        (Bridge(0, 1), Bridge(10, 1)),
        (Bridge(0, 1), Bridge(10, 1), Bridge(9, 10)),
        tuple([Bridge(0, 2)]),
        (Bridge(0, 2), Bridge(2, 3)),
        (Bridge(0, 2), Bridge(2, 3), Bridge(3, 4)),
        (Bridge(0, 2), Bridge(2, 3), Bridge(3, 5)),
        (Bridge(0, 2), Bridge(2, 2)),
        (Bridge(0, 2), Bridge(2, 2), Bridge(2, 3)),
        (Bridge(0, 2), Bridge(2, 2), Bridge(2, 3), Bridge(3, 4)),
        (Bridge(0, 2), Bridge(2, 2), Bridge(2, 3), Bridge(3, 5))
    }


def test_find_strongest_bridge():
    bridges = parse([
        "0/2",
        "2/2",
        "2/3",
        "3/4",
        "3/5",
        "0/1",
        "10/1",
        "9/10"])

    assert find_strongest_bridge(find_available_bridges(bridges)) == 31

def test_find_strength_of_longest_bridge():
    bridges = parse([
        "0/2",
        "2/2",
        "2/3",
        "3/4",
        "3/5",
        "0/1",
        "10/1",
        "9/10"])

    assert find_longest_and_strongest_bridge(find_available_bridges(bridges)) == 19
