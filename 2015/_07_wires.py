"""
--- Day 7: Some Assembly Required ---

This year, Santa brought little Bobby Tables a set of wires and bitwise logic gates! Unfortunately, little Bobby is a
little under the recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal (a number from 0 to 65535). A signal
is provided to each wire by a gate, another wire, or some specific value. Each wire can only get a signal from one
source, but can provide its signal to multiple destinations. A gate provides no signal until all of its inputs have a
signal.

The included instructions booklet describes how to connect the parts together: x AND y -> z means to connect wires x and
y to an AND gate, and then connect its output to wire z.

For example:

123 -> x means that the signal 123 is provided to wire x.

x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.

p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.

NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.

Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for some reason, you'd like to emulate the
circuit instead, almost all programming languages (for example, C, JavaScript, or Python) provide operators for these
gates.

For example, here is a simple circuit:

123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
After it is run, these are the signals on the wires:

d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456

In little Bobby's kit's instructions booklet (provided as your puzzle input), what signal is ultimately provided to wire
a?

Your puzzle answer was 956.

--- Part Two ---

Now, take the signal you got on wire a, override wire b to that signal, and reset the other wires (including wire a).
What new signal is ultimately provided to wire a?

Your puzzle answer was 40149.
"""


def parse_signal(signal):
    def parse_single_value(value):
        return ValueSignal(int(value)) if value.isnumeric() else WireSignal(value)

    def parse_operation(value):
        operations = {
            "AND": lambda a, b: a & b,
            "OR": lambda a, b: a | b,
            "LSHIFT": lambda a, b: a << b,
            "RSHIFT": lambda a, b: a >> b
        }
        return operations[value]

    def parse_signal_type(stype):
        split = stype.split(" ")
        if len(split) == 1:
            return parse_single_value(split[0])
        if len(split) == 2 and stype.startswith("NOT"):
            return NotGateSignal(parse_single_value(split[1]))
        else:
            left = parse_single_value(split[0])
            operation = parse_operation(split[1])
            right = parse_single_value(split[2])
            return LogicGateSignal(operation, left, right)

    signal_type, wire_name = signal.strip().split(" -> ")
    return Wire(wire_name, parse_signal_type(signal_type))


class Signal:

    def evaluate(self, circuit):
        raise NotImplementedError


class WireSignal(Signal):
    def __init__(self, name):
        self.name = name

    def evaluate(self, circuit):
        return circuit[self.name]


class LogicGateSignal(Signal):

    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def evaluate(self, circuit):
        return self.operation(self.left.evaluate(circuit), self.right.evaluate(circuit))


class NotGateSignal(Signal):
    def __init__(self, signal):
        self.signal = signal

    def evaluate(self, circuit):
        return int(bin(self.signal.evaluate(circuit) ^ 0b1111111111111111), base=2)


class ValueSignal(Signal):

    def __init__(self, value):
        self.value = value

    def evaluate(self, circuit):
        return self.value


class Wire:

    def __init__(self, name, signal):
        self.name = name
        self.signal = signal


class Circuit:

    def __init__(self, signal_strings):
        self.wires = ([parse_signal(signal) for signal in signal_strings])
        self.cache = {}

    def __getitem__(self, key):
        if key in self.cache:
            return self.cache[key]
        wire = list(filter(lambda w: w.name == key, self.wires))[0]
        value = wire.signal.evaluate(self)
        self.cache[key] = value
        return value

    def overwrite(self, key, value):
        wire = list(filter(lambda w: w.name == key, self.wires))[0]
        wire.signal = ValueSignal(value)
        self.cache = {}


if __name__ == "__main__":
    signals = open("_07_signals.lst").readlines()
    circuit1 = Circuit(signals)
    a_signal = circuit1["a"]

    print("Value part 1 of a is", circuit1["a"])

    circuit1.overwrite("b", a_signal)
    print("Value part2 of a is", circuit1["a"])
