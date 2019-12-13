import importlib
import pytest

module = importlib.import_module("15_dueling_generators")
generator_a = module.generator_a
generator_b = module.generator_b
picky_generator_a = module.picky_generator_a
picky_generator_b = module.picky_generator_b
is_lower_16_bits_equal = module.is_lower_16_bits_equal
judge = module.judge


def test_generator_A():
    gen = generator_a(65)

    assert next(gen) == 1092455
    assert next(gen) == 1181022009
    assert next(gen) == 245556042
    assert next(gen) == 1744312007
    assert next(gen) == 1352636452


def test_generator_B():
    gen = generator_b(8921)

    assert next(gen) == 430625591
    assert next(gen) == 1233683848
    assert next(gen) == 1431495498
    assert next(gen) == 137874439
    assert next(gen) == 285222916


def test_picky_generator_A():
    gen = picky_generator_a(65)

    assert next(gen) == 1352636452
    assert next(gen) == 1992081072
    assert next(gen) == 530830436
    assert next(gen) == 1980017072
    assert next(gen) == 740335192


def test_picky_generator_B():
    gen = picky_generator_b(8921)

    assert next(gen) == 1233683848
    assert next(gen) == 862516352
    assert next(gen) == 1159784568
    assert next(gen) == 1616057672
    assert next(gen) == 412269392


@pytest.mark.parametrize(
    "a,b,are_equal", [
        (1092455, 430625591, False),
        (1181022009, 1233683848, False),
        (245556042, 1431495498, True),
        (1744312007, 137874439, False),
        (1352636452, 285222916, False),
        (1, 1, True)])
def test_is_lower_16_bits_equal(a, b, are_equal):
    assert is_lower_16_bits_equal(a, b) == are_equal


def test_judge_part1():
    gen_a = generator_a(65)
    gen_b = generator_b(8921)

    assert judge(5, (gen_a, gen_b)) == 1


def test_judge_part2():
    gen_a = generator_a(65)
    gen_b = generator_b(8921)

    assert judge(1056, (gen_a, gen_b)) == 1
