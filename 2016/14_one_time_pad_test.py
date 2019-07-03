import importlib
import pytest

one_time_pad = importlib.import_module("14_one_time_pad")

generate_hash = one_time_pad.generate_hash
generate_stretched_hash = one_time_pad.generate_stretched_hash
has_chars_in_row = one_time_pad.has_chars_in_row
find_keys = one_time_pad.find_keys


@pytest.mark.parametrize(
    "string, index, expected", [
        ("asd", 0, "ae99c58471e70bb7b65966a70a57abf6"),
        ("asd", 1, "f5b3b9b303f5a0594272f99d191bbf45"),
        ("asd", 2, "a67995ad3ec084cb38d32725fd73d9a3"),
        ("asd", 3, "6867d9167683fb8f42558a81ad107f5b")])
def test_generate_hash(string, index, expected):
    hash_generator = generate_hash()
    assert hash_generator(string, index) == expected


@pytest.mark.parametrize(
    "string, streches, expected", [
        ("abc", 0, "577571be4de9dcce85a041ba0410f29f"),
        ("abc", 1, "eec80a0c92dc8a0777c619d9bb51e910"),
        ("abc", 2, "16062ce768787384c81fe17a7a60c7e3"),
        ("abc", 2016, "a107ff634856bb300138cac6568c0f24")])
def test_generate_stretch_hash(string, streches, expected):
    hash_generator = generate_stretched_hash(streches)
    assert hash_generator(string, 0) == expected


@pytest.mark.parametrize(
    "string, number_ofr_characters, expected", [
        ("abc", 3, None),
        ("", 2, None),
        ("aaa", 2, "a"),
        ("aaa", 3, "a"),
        ("abaaac", 3, "a"),
        ("333", 3, "3"),
        ("0034e0923cc38887a57bd7b1d4f953df", 3, "8")
    ])
def test_hash_chars_in_row(string, number_ofr_characters, expected):
    assert has_chars_in_row(string, number_ofr_characters) == expected


def test_find_keys():
    keys_finder = find_keys("abc", generate_hash())

    assert [next(keys_finder) for _ in range(3)] == [
        (39, "347dac6ee8eeea4652c7476d0f97bee5"),
        (92, "ae2e85dd75d63e916a525df95e999ea0"),
        (110, '7af7fa13b999d68bbce565971ddbae27')
    ]


def xtest_find_keys2():
    keys_finder = find_keys("abc", generate_stretched_hash(2016))
    assert next(keys_finder) == (10, "4a81e578d9f43511ab693eee1a75f194")


def xtest_find_keys_sample():
    keys_finder = find_keys("abc")
    all = [next(keys_finder) for _ in range(64)]
    print(all)
    assert all[-1] == (22728, "26ccc731a8706e0c4f979aeb341871f0")
