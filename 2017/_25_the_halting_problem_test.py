from _25_the_halting_problem import TuringMachine, sample_state_blueprint


def test_sample():
    blueprint, iterations = sample_state_blueprint()
    machine = TuringMachine(blueprint)

    checksum = machine.run(iterations)

    assert checksum == 3
