import importlib

module = importlib.import_module("16_chronal_classification")
Cmds = module.Cmds
resolve_possible_commands = module.resolve_possible_commands


def test_sample():
    step = [
        "Before: [3, 2, 1, 1]",
        "9 2 1 2",
        "After:  [3, 2, 2, 1]"
    ]

    cmds = {cmd for cmd, opcode in resolve_possible_commands(step)}

    assert len(cmds) == 3
    assert Cmds.mulr in cmds
    assert Cmds.addi in cmds
    assert Cmds.seti in cmds
