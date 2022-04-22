import pytest

from _04_secure_container import is_valid_password, \
    has_double_digit, \
    numbers_never_decrease, \
    has_no_double_digit_in_part_of_bigger_group


@pytest.mark.parametrize(
    "pswd, is_valid", [
        ("111111", True),
        ("223450", False),
        ("123789", False),
    ]
)
def test_is_valid_password_1(pswd, is_valid):
    result = is_valid_password(pswd, (has_double_digit, numbers_never_decrease))

    assert result == is_valid


@pytest.mark.parametrize(
    "pswd, is_valid", [
        ("111111", True),
        ("223450", True),
        ("123789", False),
    ]
)
def test_has_double_digit(pswd, is_valid):
    assert has_double_digit(pswd) == is_valid


@pytest.mark.parametrize(
    "pswd, is_valid", [
        ("111111", True),
        ("123456", True),
        ("223450", False),
        ("123789", True),
        ("668999", True),
    ]
)
def test_number_never_decrease(pswd, is_valid):
    assert numbers_never_decrease(pswd) == is_valid


@pytest.mark.parametrize(
    "pswd, is_valid", [
        ("111111", False),
        ("123456", False),
        ("223450", True),
        ("112233", True),
        ("123444", False),
        ("111122", True),
        ("668999", True),
        ("677778", False),
        ("677779", False),
    ]
)
def test_has_no_double_digit_in_part_of_bigger_group(pswd, is_valid):
    assert has_no_double_digit_in_part_of_bigger_group(pswd) == is_valid
