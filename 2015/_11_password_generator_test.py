import pytest

from _11_password_generator import next_password, \
    has_increasing_straight_of_three_letters, \
    has_no_forbidden_letters, \
    has_at_least_two_different_non_overlapping_pairs_of_letters


@pytest.mark.parametrize(
    "current_pswd, next_pswd", [
        ("xx", "xy"),
        ("xy", "xz"),
        ("xz", "ya"),
        ("zz", "aa")])
def test_next_password(current_pswd, next_pswd):
    assert next_password(current_pswd) == next_pswd


@pytest.mark.parametrize(
    "string, result", [
        ("abcde", True),
        ("qwexyzkd", True),
        ("abd", False)])
def test_has_increasing_straight_of_three_letters(string, result):
    assert has_increasing_straight_of_three_letters(string) == result


@pytest.mark.parametrize(
    "string, result", [
        ("avc", True),
        ("dfi", False),
        ("ulk", False),
        ("uop", False)])
def test_has_no_forbidden_letters(string, result):
    assert has_no_forbidden_letters(string) == result


@pytest.mark.parametrize(
    "string, result", [
        ("abbceffg", True),
        ("zzxx", True),
        ("abbcegjk", False),
        ("abcdfaa", False),
        ("aaaa", False)])
def test_has_at_least_two_different_non_overlapping_pairs_of_letters(string, result):
    assert has_at_least_two_different_non_overlapping_pairs_of_letters(string) == result
