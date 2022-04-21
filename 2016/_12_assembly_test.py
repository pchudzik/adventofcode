from _12_assembly import Cpu, parser


def test_cpu():
    cpu = Cpu()

    cmd = parser("cpy 41 a")
    cpu.program([cmd])

    assert cpu.registry['a'].value == 41


def test_inc():
    cpu = Cpu()

    cmd = parser("inc a")
    cpu.program([cmd])

    assert cpu.registry['a'].value == 1


def test_dec():
    cpu = Cpu()

    cmd = parser("dec a")
    cpu.program([cmd])

    assert cpu.registry['a'].value == -1


def test_jnz():
    cpu = Cpu()

    cpy_cmd = parser("cpy 1 a")
    cmd = parser("jnz a 2")
    cpu.program([cpy_cmd, cmd])

    assert cpu.stack == 3


def test_program():
    cpu = Cpu()
    cmds = [
        "cpy 41 a",
        "inc a",
        "inc a",
        "dec a",
        "jnz a 2",
        "dec a"
    ]

    cpu.program(parser(cmd) for cmd in cmds)

    assert cpu.registry['a'].value == 42
