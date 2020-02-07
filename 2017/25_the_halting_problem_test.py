import importlib

module = importlib.import_module("25_the_halting_problem")

TuringMachine = module.TuringMachine
sample_state_blueprint = module.sample_state_blueprint


def test_sample():
    blueprint,iterations = sample_state_blueprint()
    machine = TuringMachine(blueprint)

    checksum = machine.run(iterations)

    assert checksum == 3
