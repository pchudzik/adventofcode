import pytest
import importlib

module = importlib.import_module("17_spinlock")
Buffer = module.Buffer


def test_Buffer():
    buffer = Buffer(3)

    assert next(buffer) == 0
    assert next(buffer) == 1
    assert next(buffer) == 1
    assert next(buffer) == 3
    assert next(buffer) == 2
    assert next(buffer) == 1
    assert next(buffer) == 2
    assert next(buffer) == 6
    assert next(buffer) == 5


def test_part_1():
    buffer = Buffer(3)
    last = 0

    for i in range(2017):
        last = next(buffer)

    assert last == 638


def test_part_2():
    buffer = Buffer(3)

    for i in range(9):
        next(buffer)

    assert buffer.value_after(0) == 9
    assert buffer.value_after(9) == 5
    assert buffer.value_after(5) == 7
    assert buffer.value_after(7) == 2
    assert buffer.value_after(2) == 4
