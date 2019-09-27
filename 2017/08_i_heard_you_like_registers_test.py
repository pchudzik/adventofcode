import importlib
import pytest

module = importlib.import_module("08_i_heard_you_like_registers")
parse_instruction = module.parse_instruction
CPU = module.CPU
run_program = module.run_program


@pytest.mark.parametrize(
    "instruction, expected_registers", [
        ("b inc 5 if a > 1", {"a": 0, "b": 0}),
        ("b inc 5 if a < 1", {"a": 0, "b": 5}),
        ("c dec -10 if a >= 1", {"a": 0, "c": 0}),
        ("c dec -10 if a <= 0", {"a": 0, "c": 10}),
        ("c inc -20 if c == 0", {"c": -20}),
        ("c inc 20 if c != 1", {"c": 20})
    ])
def test_parse_instruction(instruction, expected_registers):
    cpu = CPU()

    cpu.execute(parse_instruction(instruction))

    assert cpu.registers == expected_registers


def test_run_program():
    cpu = run_program([
        "b inc 5 if a > 1",
        "a inc 1 if b < 5",
        "c dec -10 if a >= 1",
        "c inc -20 if c == 10",
    ])

    assert cpu.max_ever == 10
    assert cpu.registers == {
        "a": 1,
        "b": 0,
        "c": -10
    }
