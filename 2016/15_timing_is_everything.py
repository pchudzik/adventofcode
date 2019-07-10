class Disc:
    def __init__(self, *, number_of_positions, start_position):
        self.number_of_positions = number_of_positions
        self.start_position = start_position

    def position_at_time(self, time):
        pending_cycle = time % self.number_of_positions
        return (self.start_position + pending_cycle) % self.number_of_positions

    def is_fall_through(self, time):
        return self.position_at_time(time) == 0


def find_button_push_time(discs):
    time = 1
    discs = {idx: discs[idx] for idx in range(len(discs))}

    while True:
        fallthrough = all(map(
            lambda tick_disc: tick_disc[1].is_fall_through(time + tick_disc[0]),
            discs.items()))
        if fallthrough:
            return time - 1

        time += 1


if __name__ == "__main__":
    """
    Disc #1 has 17 positions; at time=0, it is at position 15.
    Disc #2 has 3 positions; at time=0, it is at position 2.
    Disc #3 has 19 positions; at time=0, it is at position 4.
    Disc #4 has 13 positions; at time=0, it is at position 2.
    Disc #5 has 7 positions; at time=0, it is at position 2.
    Disc #6 has 5 positions; at time=0, it is at position 0.
    """

    time = find_button_push_time([
        Disc(number_of_positions=17, start_position=15),
        Disc(number_of_positions=3, start_position=2),
        Disc(number_of_positions=19, start_position=4),
        Disc(number_of_positions=13, start_position=2),
        Disc(number_of_positions=7, start_position=2),
        Disc(number_of_positions=5, start_position=0)])

    print(f"part 1 = {time}")
