import pytest
import importlib

module = importlib.import_module("11_hex_ed")
shortest_path_finder = module.shortest_path_finder

@pytest.mark.parametrize(
    "path, number_of_steps",[
        ("ne,ne,ne", 3),
        ("ne,ne,sw,sw", 0),
        ("ne,ne,s,s", 2),
        ("se,sw,se,sw,sw", 3)])
def test_path_finder(path, number_of_steps):
    assert shortest_path_finder(path) == number_of_steps