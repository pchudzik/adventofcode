import pytest
import importlib

calculate_wrapping_paper_area = importlib\
    .import_module("02_wrapping_paper")\
    .calculate_wrapping_paper_area
calculate_ribbon_length = importlib\
    .import_module("02_wrapping_paper")\
    .calculate_ribbon_length


@pytest.mark.parametrize(
    "input, result", [
        (["2x3x4"], 58),
        (["1x1x10"], 43),
        (["1x1x10", "2x3x4"], 43 + 58),
    ])
def test_area_calculator(input, result):
    assert calculate_wrapping_paper_area(input) == result


@pytest.mark.parametrize(
    "input, result", [
        (["2x3x4"], 34),
        (["1x1x10"], 14),
        (["1x1x10", "2x3x4"], 34 + 14),
    ])
def test_calculate_ribbon_length(input, result):
    assert calculate_ribbon_length(input) == result
