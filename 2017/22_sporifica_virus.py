class Grid:
    def __init__(self, infected_nodes):
        self.currently_infected = set(infected_nodes)
        self.started_infection = 0

    def is_infected(self, x, y):
        return (x, y) in self.currently_infected

    def burst(self, x, y):
        if self.is_infected(x, y):
            self.cure(x, y)
        else:
            self.infect(x, y)

    def infect(self, x, y):
        self.currently_infected.add((x, y))
        self.started_infection += 1

    def cure(self, x, y):
        self.currently_infected.remove((x, y))


def parse_input(input):
    nodes = set()

    for row in range(len(input)):
        for column in range(len(input[row])):
            state = input[row][column]
            if state == "#":
                nodes.add((row, column))

    return Grid(nodes)


def find_center(input):
    center = int(len(input) / 2)
    return center, center


def next_move(grid, current_position, previous_position):
    """
    0,0 | 0,1 | 0,2
    1,0 | 1,1 | 1,2
    2,0 | 2,1,| 2,2
    """
    x, y = current_position
    xp, yp = previous_position
    is_current_infected = grid.is_infected(x, y)

    if xp == x:  # moving horizontally
        if yp < y:  # moving left
            return (x + 1, y) if is_current_infected else (x - 1, y)
        else:  # moving right
            return (x - 1, y) if is_current_infected else (x + 1, y)
    elif yp == y:  # moving vertically
        if xp < x:  # moving down
            return (x, y - 1) if is_current_infected else (x, y + 1)
        else:  # moving up
            return (x, y + 1) if is_current_infected else (x, y - 1)


def virus_carrier(iterations, starting_point, grid):
    current = starting_point
    previous = starting_point[0] + 1, starting_point[1]

    for i in range(iterations):
        current, previous = burst(current, previous, grid)


def burst(current, previous, grid):
    next = next_move(grid, current, previous)
    grid.burst(*current)
    return next, current


if __name__ == "__main__":
    with open("22_sporifica_virus.txt") as file:
        lines = list(map(str.strip, file.readlines()))
        grid = parse_input(lines)
        center = find_center(lines)

        virus_carrier(10_000, center, grid)
        print(f"part 1: {grid.started_infection}")
