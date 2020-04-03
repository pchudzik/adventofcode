class Board:
    def __init__(self):
        self.board = []
        self.current = 1

    def add_marble(self, marble):
        if marble % 23 == 0:
            self.current = self._find_position_counter_clockwise(7 + 2)
            extra_marble = self.board.pop(self.current)
            self.current = self._find_position_clockwise(2)
            return marble + extra_marble

        if len(self.board) == 0:
            self.board = [0, marble]
        elif len(self.board) == 2:
            self.board = [0, marble, *self.board[1:]]
        elif len(self.board) == 3:
            self.board = [0, *self.board[1:], marble]
        else:
            self.board.insert(self.current, marble)
            self.current = self._find_position_clockwise(2)

        return 0

    def _find_position_counter_clockwise(self, count):
        current = self.current
        for _ in range(count):
            current -= 1
            if current <= 0:
                current = len(self.board)
        return current

    def _find_position_clockwise(self, count):
        if self.current + count > len(self.board):
            return 1
        return self.current + count

    def __repr__(self):
        return ",".join(map(str, self.board)) + f" ({self.current})"


def play(board, players, marbles):
    current_player = 0
    current_marble = 1
    scores = [0] * players
    from time import time

    start = time()
    while current_marble <= marbles:
        score = board.add_marble(current_marble)
        scores[current_player] += score

        current_player += 1
        current_marble += 1

        if current_player >= players:
            current_player = 0

        if int(current_marble) % 100_000 == 0:
            now = time()
            print(f"{current_marble} out of {marbles} ({len(board.board)}) in {now - start}")
            start = time()

    return max(scores)


if __name__ == "__main__":
    max_score_1 = play(Board(), 411, 71170)
    print(f"part 1: {max_score_1}")

    max_score_2 = play(Board(), 411, 71170 * 100)
    print(f"part 2: {max_score_2}")
