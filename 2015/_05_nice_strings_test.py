import pytest

from _05_nice_strings import is_nice_string, \
    is_nice_string_improved, count_nice_strings, \
    has_pair_of_dupplicated_letters, \
    has_repeating_letter_with_one_in_between


@pytest.mark.parametrize(
    'string, is_nice', [
        ('ugknbfddgicrmopn', True),
        ('aaa', True),
        ('jchzalrnumimnmhp', False),
        ('haegwjzuvuyypxyu', False),
        ('dvszwmarrgswjxmb', False)
    ])
def test_is_nice_string(string, is_nice):
    assert is_nice_string(string) == is_nice


def test_count_nice_strings():
    input = (
        'ugknbfddgicrmopn',
        'aaa',
        'jchzalrnumimnmhp',
        'haegwjzuvuyypxyu',
        'dvszwmarrgswjxmb')

    assert count_nice_strings(input, is_nice_string) == 2


@pytest.mark.parametrize(
    'string, is_nice', [
        ('qjhvhtzxzqqjkmpb', True),
        ('xxyxx', True),
        ('uurcxstgmygtbstg', False),
        ('ieodomkazucvgmuy', False)
    ])
def test_is_nice_string_improved(string, is_nice):
    assert is_nice_string_improved(string) == is_nice


@pytest.mark.parametrize(
    'string, matches', [
        ("xyxy", True),
        ("aabcdefgaa", True),
        ("aaa", False)
    ])
def test_has_pair_of_dupplicated_letters(string, matches):
    assert has_pair_of_dupplicated_letters(string) == matches


@pytest.mark.parametrize(
    'string, matches', [
        ('xyx', True),
        ('abcdefeghi', True),
        ('aaa', True),
        ('abc', False),
        ('abca', False)])
def test_has_repeating_letter_with_one_in_between(string, matches):
    assert has_repeating_letter_with_one_in_between(string) == matches
