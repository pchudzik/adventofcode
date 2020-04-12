class Garden:
    def __init__(self, initial_state, notes):
        self._state = list(initial_state)
        self.notes = notes
        self.zero_index = 0

    def generate(self, generations):
        for _ in range(generations):
            prefix = "....."
            state = [*prefix, *self._state, *prefix]
            result = prefix
            for index in range(5, len(state) - 3):
                current_state = "".join(state[index - 2:index + 3])
                next_state = self.notes.get(current_state, ".")
                result += next_state
            result += prefix
            self.zero_index += len(prefix)
            self._state = list(result)

    @property
    def state(self):
        result = "".join(self._state)
        start, end = result.find("#"), result.rfind("#") + 1
        return result[start:end]

    @property
    def total_sum(self):
        total = 0
        for i in range(len(self._state)):
            if self._state[i] == "#":
                total += (i - self.zero_index)
        return total


def parse(puzzle):
    puzzle = [line.strip() for line in puzzle if line.strip() != ""]
    initial_state = puzzle[0].split(": ")[1]
    notes = {}
    for note in puzzle[1:]:
        state, result = note.split(" => ")
        notes[state] = result

    return Garden(initial_state, notes)


if __name__ == "__main__":
    with open("12_subterranean_sustainability.txt")as file:
        parsed = parse(file.readlines())

        parsed.generate(20)

        print(f"part 1:{parsed.total_sum}")
