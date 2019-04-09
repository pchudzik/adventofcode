import importlib
import pytest

bots = importlib.import_module("10_bots")

parse_simulation = bots.parse_simulation

simulation_steps = (
    "value 5 goes to bot 2",
    "bot 2 gives low to bot 1 and high to bot 0",
    "value 3 goes to bot 1",
    "bot 1 gives low to output 1 and high to bot 0",
    "bot 0 gives low to output 2 and high to output 0",
    "value 2 goes to bot 2"
)


def test_parse_simulation():
    simulation = parse_simulation(simulation_steps)

    assert simulation.bot(0).chips == set()
    assert simulation.bot(1).chips == {3}
    assert simulation.bot(2).chips == {5, 2}

    assert simulation.output(0) == set()
    assert simulation.output(1) == set()
    assert simulation.output(2) == set()


def test_run_simulation_steps():
    simulation = parse_simulation(simulation_steps)

    simulation.step()

    assert simulation.bot(0).chips == {5}
    assert simulation.bot(1).chips == {3, 2}
    assert simulation.bot(2).chips == set()

    assert simulation.output(0) == set()
    assert simulation.output(1) == set()
    assert simulation.output(2) == set()

    simulation.step()

    assert simulation.bot(0).chips == {5, 3}
    assert simulation.bot(1).chips == set()
    assert simulation.bot(2).chips == set()

    assert simulation.output(0) == set()
    assert simulation.output(1) == {2}
    assert simulation.output(2) == set()

    simulation.step()

    assert simulation.bot(0).chips == set()
    assert simulation.bot(1).chips == set()
    assert simulation.bot(2).chips == set()

    assert simulation.output(0) == {5}
    assert simulation.output(1) == {2}
    assert simulation.output(2) == {3}


@pytest.mark.parametrize(
    "chips, expected_bot", [
        ({2, 5}, 2),
        ({3, 2}, 1),
        ({5, 3}, 0)
    ])
def test_run_simulation(chips, expected_bot):
    simulation = parse_simulation(simulation_steps)

    bot_index = simulation.run(lambda compared_chips: compared_chips == chips)

    assert bot_index == expected_bot


@pytest.mark.parametrize(
    "outputs, expected_product", [
        ([0, 1], 10),
        ([1, 2], 6),
        ([0, 2], 15),
        ([0, 1, 2], 30)
    ])
def test_product(outputs, expected_product):
    simulation = parse_simulation(simulation_steps)

    product = simulation.run_for_product_of_outputs(outputs)

    assert product == expected_product
