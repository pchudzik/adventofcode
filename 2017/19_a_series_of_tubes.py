from collections import deque
import re


def available_paths_validator(maze):
    def predicate(visited, current, x, y):
        if x >= len(maze) or y >= len(maze[x]):
            return False

        move = maze[x][y]
        return (current, x, y) not in visited and (move.isalpha() or move in "+|-")

    return predicate


def find_all_letters(maze: str):
    pattern = re.compile(r"\w")
    return sum(len(pattern.findall(line)) for line in maze)


def walker(maze, starting_point, letters=None, visited=None):
    expected_letters_count = find_all_letters(maze)

    paths = deque([starting_point])

    if letters is None:
        letters = []
    if visited is None:
        # problem is with properly finding what already has been visited.
        # When it's simple coordinate it's not working as you can've moved to the same point from different direction
        # when moving to a point from different direction it's different "node"
        visited = set()

    check_if_path_available = available_paths_validator(maze)

    previous_move = None
    while paths:
        x, y = paths.popleft()

        if (x, y) in visited:
            break  # cycle abort look for other path?

        visited.add((previous_move, x, y))
        previous_move = x, y

        if maze[x][y].isalpha():
            letters.append(maze[x][y])
            if len(letters) >= expected_letters_count:
                return "".join(letters)

        available_moves = [
            (nx, ny)
            for nx, ny in (
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1))
            if check_if_path_available(visited, previous_move, nx, ny)]

        if len(available_moves) > 1:
            for nx, ny in available_moves:
                result = walker(maze, (nx, ny), list(letters), set(visited))
                if result:
                    return result

        paths += available_moves
