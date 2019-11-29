import importlib
import pytest

module = importlib.import_module("13_packet_scanners")

parse_firewall = module.parse_firewall
transmit_packet = module.transmit_packet
find_delay_time_without_damage = module.find_delay_time_without_damage
Firewall = module.Firewall

schematics = [
    "0: 3",
    "1: 2",
    "4: 4",
    "6: 4"
]


def test_parse_firewall():
    firewall = parse_firewall(schematics)

    assert firewall[0].depth == 3
    assert firewall[1].depth == 2
    assert firewall[4].depth == 4
    assert firewall[6].depth == 4

    for index in [0, 1, 4, 6]:
        assert firewall[index].position == 0

    assert firewall[3].is_empty
    assert firewall[5].is_empty


def test_tick_in_firewall():
    firewall = Firewall(3)

    assert firewall.position == 0

    firewall.tick()
    assert firewall.position == 1

    firewall.tick()
    assert firewall.position == 2

    firewall.tick()
    assert firewall.position == 1

    firewall.tick()
    assert firewall.position == 0

    firewall.tick()
    assert firewall.position == 1


@pytest.mark.parametrize(
    "depth, when_fail", [
        # (2, [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]),
        (3, [1, 5, 9, 13, 17, 21]),
        (4, [1, 7, 13, 19, 25, 31]),
        (5, [1, 9, 17, 25, 33, 41, 49]),
        (6, [1, 11, 21, 31, 41]),
        (7, [1, 13, 25, 37, 49])])
def test_can_pass_in_firewall(depth, when_fail):
    firewall = Firewall(depth)

    for time in range(1, max(when_fail) + 1):
        can_pass = time not in when_fail
        assert firewall.can_pass(time) == can_pass, f"for time {time} expected can_pass to be {can_pass}"


def test_transmit_packet():
    firewall = parse_firewall(schematics)

    severity = transmit_packet(firewall)

    assert severity == 24


def test_find_delay_time_without_damage():
    firewall = parse_firewall(schematics)

    assert find_delay_time_without_damage(firewall) == 10
