import re
from collections import namedtuple, defaultdict

Particle = namedtuple("Particle", "index, position, velocity, acceleration")


def find_closest_to_zero(particles, iterations=1_000):
    for i in range(iterations):
        particles = tick(particles)

    return min(
        _find_closest_to_zero(particles).items(),
        key=lambda item: item[1])[0].index


def _find_closest_to_zero(particles):
    return {particle: manhatan_distance(particle) for particle in particles}


def manhatan_distance(particle):
    return sum(map(abs, particle.position))


def tick(particles):
    return list(map(_tick_single, particles))


def _tick_single(particle):
    vx, vy, vz = particle.velocity
    ax, ay, az = particle.acceleration
    x, y, z = particle.position

    vx, vy, vz = vx + ax, vy + ay, vz + az

    return Particle(
        particle.index,
        (x + vx, y + vy, z + vz),
        (vx, vy, vz),
        particle.acceleration)


def parser(particles):
    coordinates_pattern = re.compile(r"\w=<\s*(-?\d+),(-?\d+),(-?\d+)>")

    def parse_coordinates(coordinates):
        x, y, z = coordinates_pattern.match(coordinates).groups()
        return tuple(map(int, [x, y, z]))

    result = []

    for particle_idx in range(len(particles)):
        particle = particles[particle_idx]
        position, velocity, acceleration = particle.split(", ")

        result.append(Particle(
            particle_idx,
            parse_coordinates(position),
            parse_coordinates(velocity),
            parse_coordinates(acceleration)))

    return result


if __name__ == "__main__":
    with open("20_particle_swarm.txt") as file:
        puzzle = [line.strip() for line in file.readlines()]
        particles = parser(puzzle)
        print(f"part 1: {find_closest_to_zero(particles)}")
