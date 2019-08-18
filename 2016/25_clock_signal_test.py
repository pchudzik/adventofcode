import importlib

assembly = importlib.import_module("25_clock_signal")

Cpu = assembly.Cpu
parser = assembly.parser
Value = assembly.Value
ClockSignalOutHandler = assembly.ClockSignalOutHandler


def test_cpy():
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


def test_out():
    out_values = []

    def recording_handler(value):
        out_values.append(value)
        return True

    recording_handler.can_continue = True
    recording_handler.result = True

    cpu = Cpu(
        out_handler=recording_handler,
        registry={
            'a': Value(2),
            'b': Value(3),
            'c': Value(4),
            'd': Value(5)
        })

    cpu.program([
        parser("out 1"),
        parser("out a"),
        parser("out b"),
        parser("out c"),
        parser("out d"),
    ])

    assert out_values == [1, 2, 3, 4, 5]


def test_execution_breaker():
    class EvenHandler:
        def __init__(self):
            self.can_continue = True
            self.result = True

        def __call__(self, value):
            self.can_continue = value % 2 == 0
            if not self.can_continue:
                self.result = False

    cpu = Cpu(out_handler=EvenHandler())

    result = cpu.program([
        parser("out 2"),
        parser("out 4"),
        parser("out 6"),
        parser("out 7"),
        parser("inc a"),
        parser("inc b"),
        parser("inc c"),
        parser("inc d"),
    ])

    assert result == False
    assert cpu.registry['a'].value == 0
    assert cpu.registry['b'].value == 0
    assert cpu.registry['c'].value == 0
    assert cpu.registry['d'].value == 0


def test_ClockSignalOutHandler_ok():
    handler = ClockSignalOutHandler(expected_cycle=3)

    handler(0)
    assert handler.can_continue
    assert handler.result

    handler(1)
    assert handler.can_continue
    assert handler.result

    handler(0)
    assert not handler.can_continue
    assert handler.result


def test_ClockSignalOutHandler_break():
    handler = ClockSignalOutHandler(expected_cycle=3)

    handler(0)
    assert handler.can_continue
    assert handler.result

    handler(0)
    assert not handler.can_continue
    assert not handler.result


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
