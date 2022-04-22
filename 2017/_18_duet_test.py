from _18_duet import CPU, Register, parser1, execute_part1, execute_part2

empty_snd_card = None


def test_set_cmd():
    cpu = CPU(parser1(empty_snd_card, ["set a 123"]))

    cpu.tick()

    assert cpu["a"].value == 123


def test_add_cmd():
    cpu = CPU(parser1(empty_snd_card, [
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
    cpu = CPU(parser1(empty_snd_card, [
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
    snd_card = Register(None)
    cpu = CPU(parser1(snd_card, [
        "set a 10",
        "snd a"
    ]))

    cpu.tick()
    cpu.tick()

    assert snd_card.value == 10


def test_jgz_cmd_negative():
    cpu = CPU(parser1(empty_snd_card, [
        "set a 10",
        "jgz a -1"
    ]))

    cpu.tick()
    cpu.tick()

    assert cpu.offset == 0


def test_jgz_cmd_positive():
    cpu = CPU(parser1(empty_snd_card, [
        "set a 10",
        "jgz a 1",
        "set a 11",
    ]))

    cpu.tick()
    cpu.tick()

    assert cpu.offset == 2


def test_rcv_pass_through():
    played = execute_part1([
        "rcv a",
        "set a -10",
        "rcv a"
    ])

    assert played is None


def test_stop_execution():
    played = execute_part1([
        "set a 10",
        "snd a",
        "rcv a"
    ])

    assert played == 10


def test_example():
    played = execute_part1([
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
    ])

    assert played == 4


def test_part2():
    send_values = execute_part2([
        "snd 1",
        "snd 2",
        "snd p",
        "rcv a",
        "rcv b",
        "rcv c",
        "rcv d"
    ])

    assert send_values == 3
