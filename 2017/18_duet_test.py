import importlib

module = importlib.import_module("18_duet")
CPU = module.CPU
parser = module.parser


def test_set_cmd():
    cpu = CPU(parser(["set a 123"]))

    cpu.tick()

    assert cpu["a"].value == 123


def test_add_cmd():
    cpu = CPU(parser([
        "set a 10",
        "set b 10",
        "add a b"
    ]))

    cpu.tick()
    cpu.tick()
    cpu.tick()

    assert cpu["a"].value == 20
    assert cpu["b"].value == 10


def test_mul_cmd():
    cpu = CPU(parser([
        "set a 10",
        "set b 10",
        "mul a b"
    ]))

    cpu.tick()
    cpu.tick()
    cpu.tick()

    assert cpu["a"].value == 100
    assert cpu["b"].value == 10


def test_snd_cmd():
    cpu = CPU(parser([
        "set a 10",
        "snd a"
    ]))

    cpu.tick()
    cpu.tick()

    assert cpu.played == 10


def test_jgz_cmd_negative():
    cpu = CPU(parser([
        "set a 10",
        "jgz a -1"
    ]))

    cpu.tick()
    cpu.tick()

    assert cpu.offset == 0


def test_jgz_cmd_positive():
    cpu = CPU(parser([
        "set a 10",
        "jgz a 1",
        "set a 11",
    ]))

    cpu.tick()
    cpu.tick()

    assert cpu.offset == 2


def test_rcv_pass_through():
    cpu = CPU(parser([
        "rcv a",
        "set a -10",
        "rcv a"
    ]))

    cpu.execute()

    assert cpu.offset == 3
    assert cpu.played is None


def test_stop_execution():
    cpu = CPU(parser([
        "set a 10",
        "snd a",
        "rcv a"
    ]))

    cpu.execute()

    assert cpu.offset == 2
    assert cpu.played == 10


def test_example():
    cpu = CPU(parser([
        "set a 1",
        "add a 2",
        "mul a a",
        "mod a 5",
        "snd a",
        "set a 0",
        "rcv a",
        "jgz a -1",
        "set a 1",
        "jgz a -2"
    ]))

    cpu.execute()

    assert cpu.played == 4
