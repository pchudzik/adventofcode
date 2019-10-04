class ProcessingResult:
    def __init__(self):
        self.garbage = []
        self.groups = []

    @property
    def score(self):
        return sum(score for score, *_ in self.groups)

    @property
    def removed(self):
        return sum(count for count, *_ in self.garbage)


class Token:
    def __init__(self, index):
        self.start = index
        self.end = None
        self.count = 0

    def next(self):
        self.count += 1

    def finish(self, index):
        self.end = index
        return self.count, self.start, self.end


class Group:
    def __init__(self, score, index):
        self.start = index
        self.end = None
        self.score = score

    def finish(self, index):
        self.end = index
        return self.score, self.start, self.end


def process(stream):
    result = ProcessingResult()
    groups = []
    garbage = None
    ignore = False

    for index in range(len(stream)):
        c = stream[index]

        if ignore:
            ignore = False
            continue

        if c == "!":
            ignore = True
            continue
        elif garbage is not None and c != ">":
            garbage.next()
            continue
        elif c == "<":
            garbage = Token(index)
        elif c == ">":
            result.garbage.append(garbage.finish(index))
            garbage = None
        elif c == "{":
            group = Group(len(groups) + 1, index)
            groups.append(group)
        elif c == "}":
            last_group = groups.pop()
            result.groups.append(last_group.finish(index))

    return result


if __name__ == "__main__":
    with open("09_stream_processing.txt") as file:
        puzzle = file.readline()
        processed = process(puzzle)
        print(f"part1: {processed.score}")
        print(f"part2: {processed.removed}")
