import importlib

module = importlib.import_module("23_coprocessor_conflagration")
CPU = module.CPU
Register = module.Register
parser = module.parser
execute = module.execute
MulCountingCallback = module.MulCountingCallback

def empty_callback(*args):
    pass


def test_set_cmd():
    cpu = CPU(parser(empty_callback, ["set a 123"]))

    cpu.tick()

    assert cpu["a"].value == 123


def test_mul_cmd():
    cpu = CPU(parser(empty_callback, [
        "set a 10",
        "set b 10",
        "mul a b"
    ]))

    cpu.tick()
    cpu.tick()
    cpu.tick()

    assert cpu["a"].value == 100
    assert cpu["b"].value == 10


def test_sub_cmd():
    cpu = CPU(parser(empty_callback, [
        "set a 10",
        "set b 2",
        "sub a b"
    ]))

    cpu.tick()
    cpu.tick()
    cpu.tick()

    assert cpu["a"].value == 8
    assert cpu["b"].value == 2


def test_jnz_cmd_negative():
    cpu = CPU(parser(empty_callback, [
        "set a 10",
        "jnz a -1"
    ]))

    cpu.tick()
    cpu.tick()

    assert cpu.offset == 0


def test_jnz_cmd_positive():
    cpu = CPU(parser(empty_callback, [
        "set a 10",
        "jnz a 1",
        "set a 11",
    ]))

    cpu.tick()
    cpu.tick()

    assert cpu.offset == 2


def test_stop_execution():
    all_cmds = []

    def recording_callback(*args):
        cmd = args[0]
        all_cmds.append(cmd)

    execute(parser(recording_callback, [
        "set a 10",
        "set b 10",
        "mul a b"
    ]))

    assert all_cmds == ["set", "set", "mul"]

def test_mul_counting():
    callback = MulCountingCallback()
    execute(parser(callback, [
        "set a 1",
        "set b 1",
        "mul a b",
        "mul a b",
        "mul a b"
    ]))

    assert callback.count == 3
