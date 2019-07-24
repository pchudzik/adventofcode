import importlib
import pytest

module = importlib.import_module("20_firewall_rules")

Range = module.Range
merge_ranges = module.merge_ranges
find_first_free_ip = module.find_first_free_ip
find_number_of_free_ips = module.find_number_of_free_ips


def test_parse_range():
    r = Range.parse("1-2")

    assert r.start == 1
    assert r.end == 2


def test_parse_range_order():
    with pytest.raises(ValueError):
        Range.parse("2-1")


@pytest.mark.parametrize(
    "r1, r2, overlap", [
        ((5, 8), (4, 7), True),
        ((5, 8), (0, 2), False),
        ((3, 7), (1, 3), True),
        ((3, 7), (8, 9), True),
        ((4, 9), (1, 3), True),
    ])
def test_range_overlap(r1, r2, overlap):
    r1 = Range(*r1)
    r2 = Range(*r2)

    assert r1.overlaps(r2) == overlap


def test_the_same_range_is_not_overlap():
    r1 = Range(2, 4)
    r2 = Range(2, 4)

    assert r1.overlaps(r2) == False


@pytest.mark.parametrize(
    "r1, r2, merged", [
        ((5, 8), (4, 7), (4, 8)),
        ((3, 7), (1, 3), (1, 7)),
        ((3, 7), (8, 9), (3, 9)),
        ((4, 9), (1, 3), (1, 9)),
    ])
def test_merge(r1, r2, merged):
    r1 = Range(*r1)
    r2 = Range(*r2)

    r3 = r1.merge(r2)

    assert r3.start == merged[0]
    assert r3.end == merged[1]


def test_merge_ranges():
    r1 = Range(5, 8)
    r2 = Range(0, 2)
    r3 = Range(4, 7)

    merged = merge_ranges([r1, r2, r3])

    assert len(merged) == 2
    assert Range(4, 8) in merged
    assert Range(0, 2) in merged


def test_find_first_ip():
    result = find_first_free_ip([Range(0, 2), Range(4, 8)])

    assert result == 3


@pytest.mark.parametrize(
    "available_addresses, expected", [
        (7, 2),
        (10, 5),
        (20, 15)])
def test_find_number_of_free_ips(available_addresses, expected):
    result = find_number_of_free_ips(
        [Range(0, 1), Range(3, 4), Range(6, 7)], available_addresses)

    assert result == expected
