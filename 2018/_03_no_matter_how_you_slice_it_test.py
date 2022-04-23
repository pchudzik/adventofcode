from _03_no_matter_how_you_slice_it import parse, check_overlap, find_overlapping_area, find_single_not_overlapping

puzzle = [
    "#1 @ 1,3: 4x4",
    "#2 @ 3,1: 4x4",
    "#3 @ 5,5: 2x2",
]


def test_parse():
    result = parse(puzzle)
    assert len(result) == 3
    c1, c2, c3 = result

    assert c1.id == 1
    assert c1.x1, c1.y1 == (1, 3)
    assert c1.x2, c1.y2 == (5, 7)

    assert c2.id == 2
    assert c2.x1, c2.y1 == (3, 1)
    assert c2.x2, c2.y2 == (5, 5)

    assert c3.id == 3
    assert c3.x1, c3.y1 == (5, 5)
    assert c3.x2, c3.y2 == (7, 7)


def test_overlap():
    c1, c2, c3 = parse(puzzle)

    assert not check_overlap(c1, c3)
    assert not check_overlap(c2, c3)

    assert check_overlap(c1, c2)


def test_find_all_overlapping():
    claims = parse(puzzle)

    assert find_overlapping_area(claims) == 4


def test_find_single_not_overlapping():
    claims = parse(puzzle)

    assert find_single_not_overlapping(claims) == claims[2]
