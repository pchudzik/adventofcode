import importlib
import pytest

registers_module = importlib.import_module("23_registers")
parse_operations = registers_module.parse_operations
Program = registers_module.Program


@pytest.mark.parametrize(
    "initial_offset, a, b, instructions, expected_offset, expected_a, expected_b", [
        (0, 6, 4, ["hlf a"], 1, 3, 4),
        (0, 7, 4, ["hlf a"], 1, 3, 4),
        (0, 7, 0, ["hlf b"], 1, 7, 0),
        (0, 2, 0, ["tpl a"], 1, 6, 0),
        (0, 0, 0, ["tpl a"], 1, 0, 0),
        (0, 0, 0, ["inc a"], 1, 1, 0),
        (0, 0, 0, ["inc a", "jmp -1"], 0, 1, 0),
        (0, 0, 0, ["jmp +1", "inc a", ], 2, 1, 0),
        (0, 0, 0, ["jie a, +1", "inc a", ], 2, 1, 0),
        (0, 0, 0, ["inc a", "jie a, -1"], 2, 1, 0),
        (0, 0, 0, ["jio a, 10"], 1, 0, 0),
        (0, 1, 0, ["jio a, 10"], 10, 1, 0),
    ]
)
def test_parse_operations(initial_offset, a, b, instructions, expected_offset, expected_a, expected_b):
    program = Program(a=a, b=b, offset=initial_offset)
    operations = parse_operations(instructions)

    for operation in operations:
        operation(program)

    assert len(operations) == len(instructions)
    assert program.a == expected_a
    assert program.b == expected_b
    assert program.offset == expected_offset


def test_program():
    operations = parse_operations([
        "inc a",
        "jio a, +2",
        "tpl a",
        "inc a"
    ])
    program = Program()

    program.process(operations)
    assert program.a == 2

