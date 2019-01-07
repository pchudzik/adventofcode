import pytest
import importlib

Circuit = importlib\
    .import_module('07_wires')\
    .Circuit


@pytest.mark.parametrize(
    "wire_name, expected_vale", [
        ("d", 72),
        ("e", 507),
        ("f", 492),
        ("g", 114),
        ("h", 65412),
        ("i", 65079),
        ("x", 123),
        ("y", 456)
    ])
def test_calculate_values(wire_name, expected_vale):
    circuit_input = [
        "123 -> x",
        "456 -> y",
        "x AND y -> d",
        "x OR y -> e",
        "x LSHIFT 2 -> f",
        "y RSHIFT 2 -> g",
        "NOT x -> h",
        "NOT y -> i"
    ]

    circuit = Circuit(circuit_input)

    assert circuit[wire_name] == expected_vale


def test_wires_example_1():
    circuit = Circuit(["123 -> x"])

    assert circuit["x"] == 123


def test_wires_example_2():
    circuit = Circuit([
        "123 -> x",
        "321 -> y",
        "x AND y -> z"
    ])

    assert circuit["x"] == 123
    assert circuit["y"] == 321
    assert circuit["z"] == 65


def test_wires_example_3():
    circuit = Circuit([
        "222 -> p",
        "p LSHIFT 2 -> q"
    ])

    assert circuit["p"] == 222
    assert circuit["q"] == 888


def test_wires_example_4():
    circuit = Circuit([
        "NOT e -> f",
        "1 -> e"
    ])

    assert circuit["e"] == 1
    assert circuit["f"] == 65534


@pytest.mark.parametrize(
    "circuit_input, wire, expected_vale", [
        (["1 -> x"], "x", 1),
        (["1 -> x", "x -> y"], "y", 1)
    ])
def test_simple_value_evaluation(circuit_input, wire, expected_vale):
    circuit = Circuit(circuit_input)

    assert circuit[wire] == expected_vale
