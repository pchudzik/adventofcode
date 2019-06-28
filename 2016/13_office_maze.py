class Maze:
    def __init__(self, size, favorite_number):
        self.max_x = size[0]
        self.max_y = size[1]
        self.favorite_number = favorite_number

        self.maze = self.generate_maze()

    def generate_maze(self):
        maze = [[False] * self.max_x for _ in range(self.max_y)]
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                value = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + self.favorite_number
                value = format(value, 'b').count('1') % 2
                maze[y][x] = value == 0
        return maze

    def shortest_path(self, end):
        queue = []
        shortest_path = None
        visited = set()
        visited.add((1, 1))
        queue.append((1, 1, 0))

        while queue:
            x, y, distance = queue.pop(0)
            if (x, y) == end:
                if not shortest_path or shortest_path > distance:
                    shortest_path = distance

            possible_moves = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1)
            ]

            possible_moves = [
                (pos_x, pos_y)
                for pos_x, pos_y in possible_moves
                if self._is_valid_coordinate(pos_x, pos_y) and (pos_x, pos_y) not in visited and self.maze[pos_y][pos_x]
            ]

            for move in possible_moves:
                pos_x, pos_y = move
                visited.add((pos_x, pos_y))
                queue.append((pos_x, pos_y, distance + 1))

        return shortest_path

    def _is_valid_coordinate(self, x, y):
        return 0 <= x < self.max_x and 0 <= y < self.max_y

    def __repr__(self):
        result = ""
        for row in self.maze:
            for space in row:
                result += "." if space else "#"
            result += "\n"
        return result.strip()


if __name__ == "__main__":
    favorite_number = 1362
    maze = Maze((100, 100), favorite_number)
    print("part1", maze.shortest_path((31, 39)))

