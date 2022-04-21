from _23_safe_cracking import Cpu, Value, parser


def test_cpy():
    cmd = parser("cpy 41 a")
    cpu = Cpu([cmd])

    cpu.run()

    assert cpu.registry['a'].value == 41


def test_inc():
    cmd = parser("inc a")
    cpu = Cpu([cmd])

    cpu.run()

    assert cpu.registry['a'].value == 1


def test_dec():
    cmd = parser("dec a")
    cpu = Cpu([cmd])

    cpu.run()

    assert cpu.registry['a'].value == -1


def test_jnz():
    cpy_cmd = parser("cpy 1 a")
    cmd = parser("jnz a 2")

    cpu = Cpu([cpy_cmd, cmd])
    cpu.run()

    assert cpu.stack == 3


def test_tgl_inc():
    cpu = Cpu([parser("tgl 1"), parser("inc a")])

    cpu.run()

    assert cpu.registry['a'].value == -1


def test_tgl_dec():
    cpu = Cpu([parser("tgl 1"), parser("dec a")])

    cpu.run()

    assert cpu.registry['a'].value == 1


def test_tgl_jnz():
    cpu = Cpu(
        [
            parser("tgl 1"),
            parser("jnz b a"),
            parser("inc a")],
        registry={
            'a': Value(1),
            'b': Value(10),
            'c': Value(0),
            'd': Value(0)
        })

    cpu.run()

    assert cpu.registry['a'].value == 11


def test_tgl_cpy():
    cpu = Cpu(
        [
            parser("tgl 1"),
            parser("cpy b a"),
            parser("inc a"),
            parser("dec a")],
        registry={
            'a': Value(2),
            'b': Value(10),
            'c': Value(0),
            'd': Value(0)
        })

    cpu.run()

    assert cpu.registry['a'].value == 1


def test_tgl_tgl():
    cpu = Cpu(
        [
            parser("tgl a"),
            parser("tgl a")],
        registry={
            'a': Value(1),
            'b': Value(0),
            'c': Value(0),
            'd': Value(0)
        })

    cpu.run()

    assert cpu.registry['a'].value == 2


def test_tgl_out_of_scope():
    cpu = Cpu([
        parser("tgl 100"),
        parser("inc a")])

    cpu.run()

    assert cpu.registry['a'].value == 1


def test_mul():
    cpu = Cpu([parser("cpy 10 b"), parser("cpy 10 d"), parser("mul b d a")])

    cpu.run()

    assert cpu.registry['a'].value == 100


def test_program():
    cmds = [
        "cpy 41 a",
        "inc a",
        "inc a",
        "dec a",
        "jnz a 2",
        "dec a"
    ]

    cpu = Cpu(parser(cmd) for cmd in cmds)
    cpu.run()

    assert cpu.registry['a'].value == 42


def test_program_tgl():
    cmds = [
        "cpy 2 a",
        "tgl a",
        "tgl a",
        "tgl a",
        "cpy 1 a",
        "dec a",
        "dec a"
    ]

    cpu = Cpu(parser(cmd) for cmd in cmds)
    cpu.run()

    assert cpu.registry['a'].value == 3
