import pytest
import importlib

is_triangle_possible = importlib.import_module("03_triangle").is_triangle_possible
parse_triangle = importlib.import_module("03_triangle").parse_triangle
count_valid_triangles = importlib.import_module("03_triangle").count_valid_triangles
count_valid_vertical_triangles = importlib.import_module("03_triangle").count_valid_vertical_triangles


@pytest.mark.parametrize(
    "triangle, is_possible", [
        ([5, 10, 25], False),
        ([10, 5, 25], False),
        ([25, 10, 5], False),
        ([9, 10, 5], True)])
def test_is_triangle_possible(triangle, is_possible):
    assert is_triangle_possible(triangle) == is_possible


def test_parse_triangle():
    assert parse_triangle("  607  425  901") == (607, 425, 901)


def test_count_invalid_triangles():
    triangles = (
        "  607  425  901  ",
        "    5   10   25  ")

    assert count_valid_triangles(triangles) == 1


def test_count_valid_vertical_triangles():
    triangles = (
        "101 301 501",
        "102 302 502",
        "103 303 503",
        "201 401 601",
        "202 402 602",
        "203 403 603"
    )

    assert count_valid_vertical_triangles(triangles) == 6
