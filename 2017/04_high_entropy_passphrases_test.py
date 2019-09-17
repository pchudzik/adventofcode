import importlib
import pytest

module = importlib.import_module("04_high_entropy_passphrases")
has_no_duplicated_words = module.has_no_duplicated_words
has_no_anagrams = module.has_no_anagrams
find_valid_passphases = module.find_valid_passphases


@pytest.mark.parametrize(
    "password, expected", [
        ("aa bb cc dd ee", True),
        ("aa bb cc dd aa", False),
        ("aa bb cc dd aaa", True)])
def test_has_no_duplicated_words(password, expected):
    assert has_no_duplicated_words(password) == expected


@pytest.mark.parametrize(
    "password, expected", [
        ("abcde fghij", True),
        ("abcde xyz ecdab", False),
        ("a ab abc abd abf abj", True),
        ("iiii oiii ooii oooi oooo", True),
        ("oiii ioii iioi iiio", False),
        ("refpcz uqt uqt uqt", False)
    ])
def test_has_no_anagrams(password, expected):
    assert has_no_anagrams(password) == expected


def test_find_valid_passphases_no_duplicated_words():
    assert find_valid_passphases(
        has_no_duplicated_words,
        (
            "aa bb cc dd ee",
            "aa bb cc dd aa",
            "aa bb cc dd aaa")) == [
               "aa bb cc dd ee",
               "aa bb cc dd aaa"]


def test_find_valid_passphases_no_anagrams():
    assert find_valid_passphases(
        has_no_anagrams,
        (
            "abcde fghij",
            "abcde xyz ecdab",
            "a ab abc abd abf abj",
            "iiii oiii ooii oooi oooo",
            "oiii ioii iioi iiio")) == [
               "abcde fghij",
               "a ab abc abd abf abj",
               "iiii oiii ooii oooi oooo"]
