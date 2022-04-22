import pytest

from _13_packet_scanners import parse_firewall, transmit_packet, find_delay_time_without_damage, firewall_layer

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

    assert not firewall[0](0)
    assert not firewall[1](0)
    assert firewall[2](0)
    assert firewall[3](0)
    assert not firewall[4](0)
    assert firewall[5](0)
    assert not firewall[6](0)


@pytest.mark.parametrize(
    "depth, when_fail", [
        (2, [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]),
        (3, [0, 4, 8, 12, 16, 20]),
        (4, [0, 6, 12, 18, 24, 30]),
        (5, [0, 8, 16, 24, 32, 40, 48]),
        (6, [0, 10, 20, 30, 40]),
        (7, [0, 12, 24, 36, 48])])
def test_can_pass_in_firewall(depth, when_fail):
    firewall = firewall_layer(depth)

    for time in range(1, max(when_fail) + 1):
        can_pass = time not in when_fail
        assert firewall(time) == can_pass, f"for time {time} expected can_pass to be {can_pass}"


def test_transmit_packet():
    firewall = parse_firewall(schematics)

    severity = transmit_packet(firewall)

    assert severity == 24


def test_find_delay_time_without_damage():
    firewall = parse_firewall(schematics)

    assert find_delay_time_without_damage(firewall) == 10
