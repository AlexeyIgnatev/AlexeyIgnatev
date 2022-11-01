import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 15, speed: int = 15) -> None:
        self.cell_size = cell_size
        self.life = life
        self.height = self.cell_size * self.life.cell_height
        self.width = self.cell_size * self.life.cell_width

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.speed = speed

        super().__init__(life)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))
        return None

    def draw_grid(self) -> None:
        for y in range(self.life.cell_height):
            for x in range(self.life.cell_width):
                color = pygame.Color("green") if self.life.curr_generation[y][x] else pygame.Color("white")
                pygame.draw.rect(self.screen, color,
                                 (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        return None

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()
            self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


GUI(GameOfLife((50, 50))).run()
