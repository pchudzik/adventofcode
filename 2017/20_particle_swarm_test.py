import importlib

module = importlib.import_module("20_particle_swarm")
parser = module.parser
tick = module.tick
manhatan_distance = module.manhatan_distance
find_closest_to_zero = module.find_closest_to_zero


def test_find_closes_to_zero():
    particles = parser([
        "p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>",
        "p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"
    ])

    particle = find_closest_to_zero(particles, iterations=100)

    assert particle == 0


def test_manhatan_distance():
    p0, p1 = parser([
        "p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>",
        "p=<-5,-2,-2>, v=<0,0,0>, a=<0,0,0>"
    ])

    assert manhatan_distance(p0) == 3
    assert manhatan_distance(p1) == 9


def test_particle_parser():
    raw = [
        "p=<-3,-4,-5>, v=<-2,-1,-10>, a=<-1,-220,-224>",
        "p=< 4,3,2>, v=< 1,2,3>, a=<2,4,6>"
    ]

    result = parser(raw)

    p0, p1 = result

    assert p0.index == 0
    assert p0.position == (-3, -4, -5)
    assert p0.velocity == (-2, -1, -10)
    assert p0.acceleration == (-1, -220, -224)

    assert p1.index == 1
    assert p1.position == (4, 3, 2)
    assert p1.velocity == (1, 2, 3)
    assert p1.acceleration == (2, 4, 6)


def test_tick_particles():
    particles = parser([
        "p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>",
        "p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"])

    p0, p1 = tick(particles)

    assert p0.position == (4, 0, 0)
    assert p0.velocity == (1, 0, 0)
    assert p0.acceleration == (-1, 0, 0)

    assert p1.position == (2, 0, 0)
    assert p1.velocity == (-2, 0, 0)
    assert p1.acceleration == (-2, 0, 0)

    p0, p1 = tick([p0, p1])

    assert p0.position == (4, 0, 0)
    assert p0.velocity == (0, 0, 0)
    assert p0.acceleration == (-1, 0, 0)

    assert p1.position == (-2, 0, 0)
    assert p1.velocity == (-4, 0, 0)
    assert p1.acceleration == (-2, 0, 0)

    p0, p1 = tick([p0, p1])

    assert p0.position == (3, 0, 0)
    assert p0.velocity == (-1, 0, 0)
    assert p0.acceleration == (-1, 0, 0)

    assert p1.position == (-8, 0, 0)
    assert p1.velocity == (-6, 0, 0)
    assert p1.acceleration == (-2, 0, 0)
