def pattern_reader(pattern):
    return pattern.replace("/", "\n")


def pattern_variants(pattern):
    def upside_down(pattern):
        return pattern[::-1]

    def mirror(pattern):
        return [line[::-1] for line in pattern]

    def flip(pattern):
        result = []
        for i in range(len(pattern)):
            column = ""
            for j in range(len(pattern[i])):
                column += pattern[j][i]
            result.append(column[::-1])
        return result

    def variants(pattern):
        pattern = pattern.split("\n")
        yield pattern
        yield upside_down(pattern)
        yield mirror(pattern)
        yield flip(pattern)

    return map(lambda l: "\n".join(l), variants(pattern))


def divide_pattern(pattern, size):
    pattern = pattern.split("\n")
    length = len(pattern)
    for row in range(0, length, size):
        result = []
        for column in range(0, length, size):
            tmp = [pattern[x][column:column + size] for x in range(row, row + size)]
            result.append("\n".join(tmp))
        yield result

def join_pattern(patterns):
    pass

def transform(initial, rules, iterations):
    for iteration in range(iterations):
        if len(initial) % 2 == 0:
            pass