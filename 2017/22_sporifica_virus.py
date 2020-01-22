class Grid:
    def __init__(self, infected_nodes):
        self.initially_infected = set(infected_nodes)
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
        if (x, y) not in self.initially_infected:
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
    -1, 1  | 0, 1   | 1, 1
    -1, 0  | 0, 0   | 1, 0
    -1, -1 | 0, -1  | 1, -1
    """
    x, y = current_position
    xp, yp = previous_position
    is_current_infected = grid.is_infected(x, y)

    if xp == x:  # moving vertically
        if yp > y:  # moving down
            return (x - 1, y) if is_current_infected else (x + 1, y)
        else:  # moving up
            return (x + 1, y) if is_current_infected else (x - 1, y)
    elif yp == y:  # moving horizontally
        if xp > x:  # moving left
            return (x, y + 1) if is_current_infected else (x, y - 1)
            pass
        else:  # moving right
            return (x, y - 1) if is_current_infected else (x, y + 1)


def virus_carrier(iterations, starting_point, grid):
    current = starting_point
    previous = starting_point[0], starting_point[1] - 1

    for i in range(iterations):
        current, previous = burst(current, previous, grid)


def burst(current, previous, grid):
    next = next_move(grid, current, previous)
    grid.burst(*current)
    return next, current
