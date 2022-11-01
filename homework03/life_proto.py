import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        return [
            [random.randrange(2) if randomize else 0 for _ in range(self.cell_width)]
            for _ in range(self.cell_height)
        ]

    def draw_grid(self) -> None:
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        n = []

        i = cell[0]
        j = cell[1]

        if i - 1 >= 0 and j - 1 >= 0:
            n.append(self.grid[i - 1][j - 1])

        if i - 1 >= 0:
            n.append(self.grid[i - 1][j])

        if i - 1 >= 0 and j + 1 < self.cell_width:
            n.append(self.grid[i - 1][j + 1])

        if j + 1 < self.cell_width:
            n.append(self.grid[i][j + 1])

        if i + 1 < self.cell_height and j + 1 < self.cell_width:
            n.append(self.grid[i + 1][j + 1])

        if i + 1 < self.cell_height:
            n.append(self.grid[i + 1][j])

        if i + 1 < self.cell_height and j - 1 >= 0:
            n.append(self.grid[i + 1][j - 1])

        if j - 1 >= 0:
            n.append(self.grid[i][j - 1])

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
                    grid[i][j] = self.grid[i][j]

        return grid
