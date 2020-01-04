import importlib
import pytest

module = importlib.import_module("19_a_series_of_tubes")
walker = module.walker
is_going_vertically = module.is_going_vertically
is_going_horizontally = module.is_going_horizontally


@pytest.mark.parametrize(
    "previous, current, is_vertical", [
        ((0, 0), (1, 0), True),
        ((1, 0), (-1, 0), True),
        (None, (1, 0), True),
        ((0, 0), (1, 1), False)])
def test_detect_when_going_vertically(previous, current, is_vertical):
    any_maze = ["   ", "   "]

    assert is_going_vertically(any_maze, current, previous) == is_vertical


def test_detect_when_going_vertically_when_crossroad():
    maze = ["+"]

    assert is_going_horizontally(maze, (0, 0), None) is False


@pytest.mark.parametrize(
    "previous, current, is_vertical", [
        ((0, 0), (0, 1), True),
        ((1, 1), (1, -1), True),
        (None, (1, 0), True),
        ((0, 0), (1, 1), False)])
def test_detect_when_going_horizontally(previous, current, is_vertical):
    any_maze = ["   ", "   "]

    assert is_going_horizontally(any_maze, current, previous) == is_vertical


def test_detect_when_going_horizontally_when_crossroad():
    maze = ["+"]

    assert is_going_horizontally(maze, (0, 0), None) is False


def test_example():
    example = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
    """.split("\n")

    path, moves = walker(example, (0, 5))

    assert path == "ABCDEF"
    assert moves == 38
