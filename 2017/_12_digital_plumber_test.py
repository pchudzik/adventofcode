from _12_digital_plumber import parse_pipes, count_programs_with_access_to, find_number_of_groups

pipes = [
    "0 <-> 2",
    "1 <-> 1",
    "2 <-> 0, 3, 4",
    "3 <-> 2, 4",
    "4 <-> 2, 3, 6",
    "5 <-> 6",
    "6 <-> 4, 5",
]


def test_parse_pipes():
    parsed = parse_pipes(pipes)

    assert parsed[0].connection_ids == [2]
    assert parsed[1].connection_ids == [1]
    assert parsed[2].connection_ids == [0, 3, 4]
    assert parsed[3].connection_ids == [2, 4]
    assert parsed[4].connection_ids == [2, 3, 6]
    assert parsed[5].connection_ids == [6]
    assert parsed[6].connection_ids == [4, 5]


def test_pipe_can_access():
    parsed = parse_pipes(pipes)

    assert parsed[0].can_access(0) is True
    assert parsed[2].can_access(0) is True
    assert parsed[3].can_access(0) is True
    assert parsed[4].can_access(0) is True
    assert parsed[5].can_access(0) is True
    assert parsed[6].can_access(0) is True

    assert parsed[1].can_access(0) is False


def test_count_programs_with_access_to():
    parsed = parse_pipes(pipes)

    assert count_programs_with_access_to(parsed.values(), 0) == 6


def test_pipe_programs_in_group():
    parsed = parse_pipes(pipes)

    assert parsed[0].programs_in_group() == {0, 2, 3, 4, 5, 6}
    assert parsed[2].programs_in_group() == {0, 2, 3, 4, 5, 6}
    assert parsed[3].programs_in_group() == {0, 2, 3, 4, 5, 6}
    assert parsed[4].programs_in_group() == {0, 2, 3, 4, 5, 6}
    assert parsed[5].programs_in_group() == {0, 2, 3, 4, 5, 6}
    assert parsed[6].programs_in_group() == {0, 2, 3, 4, 5, 6}

    assert parsed[1].programs_in_group() == {1}


def test_find_number_of_groups():
    parsed = parse_pipes(pipes)

    assert find_number_of_groups(parsed.values()) == 2
