import pytest
import importlib


find_number_for_hash_code_with_at_least_X_leading_zeros = importlib\
    .import_module("04_miner")\
    .find_number_for_hash_code_with_at_least_X_leading_zeros


@pytest.mark.parametrize(
    'secret, number', [
        ('abcdef', 298),
        ('pqrstuv', 53)
    ])
def test_find_number_for_hash_code_with_at_least_5_leading_zeros(secret, number):
    assert find_number_for_hash_code_with_at_least_X_leading_zeros(
        secret, 2) == number
