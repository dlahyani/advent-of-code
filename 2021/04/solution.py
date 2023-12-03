class BingoBoard:
    def __init__(self, raw_board: list[str]):
        self._board = [[int(n) for n in r.split(" ") if n != ""] for r in raw_board.split("\n")]
        self._board_map = {}
        for i in range(5):
            for j in range(5):
                n = self._board[i][j]
                self._board_map[n] = (i, j, False)

        self._rows_mark_counter = [0] * 5
        self._cols_mark_counter = [0] * 5
        self._last_mark = None

    def mark(self, n: int) -> bool:
        if n not in self._board_map:
            return False

        self._last_mark = n
        d = list(self._board_map[n])
        row, col = d[0:2]
        d[2] = True
        self._board_map[n] = tuple(d)
        self._rows_mark_counter[row] += 1
        self._cols_mark_counter[col] += 1

        if self._rows_mark_counter[row] == 5 or self._cols_mark_counter[col] == 5:
            return True

        return False

    @property
    def is_winning(self) -> bool:
        return 5 in self._rows_mark_counter + self._cols_mark_counter

    @property
    def marks(self) -> list[int]:
        return list(filter(lambda n: self._board_map[n][2], self._board_map))

    @property
    def unmarked_numbers(self):
        return list(filter(lambda n: not self._board_map[n][2], self._board_map))

    @property
    def score(self) -> int:
        if not self.is_winning:
            raise ValueError()

        return sum(self.unmarked_numbers) * self._last_mark

    def __str__(self):
        rows = [" ".join([f"{n:>2}" for n in row]) for row in self._board]
        return "\n".join(rows)


with open("2021/04/input.txt") as f:
    data = f.read()

sections = data.split("\n\n")
drawn_numbers = [int(n) for n in sections[0].split(",")]
boards = [BingoBoard(b) for b in sections[1:]]

first_winning_board = None
last_winning_board = None
for n in drawn_numbers:
    for b in boards.copy():
        if b.mark(n):
            boards.remove(b)
            if not first_winning_board:
                first_winning_board = b

    if len(boards) == 1:
        last_winning_board = b

print(f"First winning board:\n{first_winning_board}")
print(f"marks: {first_winning_board.marks}, score: {first_winning_board.score}")

print(f"Last winning board:\n{last_winning_board}")
print(f"marks: {last_winning_board.marks}, score: {last_winning_board.score}")
