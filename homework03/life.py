import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self,
            size: tp.Tuple[int, int],
            randomize: bool = True,
            max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size

        self.cell_height = size[0]
        self.cell_width = size[1]

        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        return [[random.randrange(2) if randomize else 0 for _ in range(self.cell_width)] for _ in
                range(self.cell_height)]

    def get_neighbours(self, cell: Cell) -> Cells:
        n = []

        i = cell[0]
        j = cell[1]

        if i - 1 >= 0 and j - 1 >= 0:
            n.append(self.curr_generation[i - 1][j - 1])

        if i - 1 >= 0:
            n.append(self.curr_generation[i - 1][j])

        if i - 1 >= 0 and j + 1 < self.cell_width:
            n.append(self.curr_generation[i - 1][j + 1])

        if j + 1 < self.cell_width:
            n.append(self.curr_generation[i][j + 1])

        if i + 1 < self.cell_height and j + 1 < self.cell_width:
            n.append(self.curr_generation[i + 1][j + 1])

        if i + 1 < self.cell_height:
            n.append(self.curr_generation[i + 1][j])

        if i + 1 < self.cell_height and j - 1 >= 0:
            n.append(self.curr_generation[i + 1][j - 1])

        if j - 1 >= 0:
            n.append(self.curr_generation[i][j - 1])

        return n

    def get_next_generation(self) -> Grid:

        grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                s = sum(self.get_neighbours((i, j)))
                if s == 3:
                    grid[i][j] = 1
                elif s < 2 or s > 3:
                    grid[i][j] = 0
                else:
                    grid[i][j] = self.curr_generation[i][j]

        return grid

    def step(self) -> None:
        new_gen = self.get_next_generation()
        self.generations += 1

        self.prev_generation = self.curr_generation
        self.curr_generation = new_gen

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.prev_generation[i][j] != self.curr_generation[i][j]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename) as f:
            grid = f.readlines()
            height = len(grid)
            width = len(grid[0].strip())

            for i in range(len(grid)):
                grid[i] = list(map(int, [*(grid[i].strip())]))

        life = GameOfLife((height, width))
        life.curr_generation = grid
        return life

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as f:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    f.write(str(self.curr_generation[i][j]))
                f.write("\n")
        return None
