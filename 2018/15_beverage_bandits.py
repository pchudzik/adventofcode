from collections import deque, defaultdict


class Board:
    def __init__(self, units, walls):
        self._units = set(units)
        self.walls = set(walls)
        self.rounds = 0

    @property
    def units(self):
        return [unit for unit in self._units if unit.is_alive]

    def tick(self):
        units_in_order = sorted(self.units, key=sort_by_reading_order)
        for unit in units_in_order:
            if unit.is_alive:
                unit.do_turn(self)
        self.rounds += 1

    @property
    def remaining_hit_points(self):
        return sum(unit.hp for unit in self.units)

    @property
    def _blocked_spaces(self):
        return self.walls | {unit.position for unit in self.units}

    @property
    def elves(self):
        return sorted(
            (unit for unit in self.units if unit.type == "E"),
            key=sort_by_reading_order)

    @property
    def goblins(self):
        return sorted(
            (unit for unit in self.units if unit.type == "G"),
            key=sort_by_reading_order)

    def find_closest_enemy(self, position, enemy_type):
        enemies = [unit for unit in self.units if unit.type == enemy_type]
        self._check_game_over(enemies)

        attack_positions = {
            (position[0], position[1] + 1),
            (position[0], position[1] - 1),
            (position[0] + 1, position[1]),
            (position[0] - 1, position[1])
        }
        enemies_in_range = [enemy for enemy in enemies if enemy.position in attack_positions]
        if len(enemies_in_range) > 0:
            lowest_hp = min(enemies_in_range, key=lambda e: e.hp).hp
            return sorted(
                [enemy for enemy in enemies_in_range if enemy.hp == lowest_hp],
                key=sort_by_reading_order)[0]
        return None

    def find_path_to_enemy(self, position, enemy_type):
        enemies = sorted(
            [unit for unit in self.units if unit.type == enemy_type],
            key=sort_by_reading_order)
        self._check_game_over(enemies)

        distances = defaultdict(list)
        for enemy in enemies:
            x, y = enemy.position
            possible_attack_points = [
                (x, y + 1),
                (x, y - 1),
                (x + 1, y),
                (x - 1, y)
            ]

            if position in possible_attack_points:
                return enemy, []

            possible_attack_points = [
                attack_point
                for attack_point in possible_attack_points
                if self._is_open_space(attack_point)]

            if len(possible_attack_points) == 0:
                continue
            shortest_path = None
            for attack_point in sorted(possible_attack_points, key=sort_by_reading_order):
                path = self._find_path(position, attack_point)
                if path is None:
                    continue

                if shortest_path is None:
                    shortest_path = path

                if len(path) < len(shortest_path):
                    shortest_path = path

            if shortest_path is None:
                continue

            distances[len(shortest_path)].append((enemy, shortest_path))
        if len(distances) >= 1:
            closest_enemies = min(distances.keys())
            enemy_to_path = {enemy: path for enemy, path in distances[closest_enemies]}
            closest_enemy = sorted(enemy_to_path.keys(), key=sort_by_reading_order)[0]
            return enemy_to_path[closest_enemy]

        return None

    @staticmethod
    def _check_game_over(enemies):
        if len(enemies) == 0:
            raise StopIteration

    def _find_path(self, start, end):
        queue = deque()
        visited = set()
        visited.add(start)
        queue.append((*start, 0, []))

        while queue:
            x, y, distance, path = queue.popleft()
            if (x, y) == end:
                return path

            possible_moves = sorted([
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ], key=sort_by_reading_order)

            possible_moves = [
                loc
                for loc in possible_moves
                if self._is_open_space(loc) and loc not in visited
            ]

            for move in possible_moves:
                visited.add(move)
                new_path = list(path)
                new_path.append(move)
                queue.append((*move, distance + 1, new_path))

    def _is_open_space(self, location):
        return location not in self._blocked_spaces


def sort_by_reading_order(unit):
    if hasattr(unit, "position"):
        x, y = unit.position
    else:
        x, y = unit
    return x + y * 10


class Unit:
    def __init__(self, type, position):
        self.type = type
        self.position = position
        self.damage = 3
        self.hp = 200
        self.enemy = "E" if type == "G" else "G"

    @property
    def is_alive(self):
        return self.hp > 0

    def do_turn(self, board: Board):
        attacked = self._try_attack(board)
        if not attacked:
            path = board.find_path_to_enemy(self.position, self.enemy)
            if path:
                self.position = path[0]
            self._try_attack(board)

    def _try_attack(self, board: Board):
        enemy = board.find_closest_enemy(self.position, self.enemy)
        if enemy:
            enemy.hp -= self.damage
            return True

    def __repr__(self):
        return f"{self.type} {self.position} [{self.hp}]"


def parse(puzzle):
    walls = []
    units = []

    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            item = puzzle[y][x]
            if item == "#":
                walls.append((x, y))
            elif item in "EG":
                units.append(Unit(item, (x, y)))
    return Board(units, walls)


def play_game(board: Board):
    while True:
        try:
            board.tick()
            print(f"turns {board.rounds}, units {board.units}")
        except StopIteration:
            return board.rounds * board.remaining_hit_points


if __name__ == "__main__":
    with open("15_beverage_bandits.txt") as file:
        board = parse(file.readlines())
        score = play_game(board)

        print(f"part 1: {score}")
