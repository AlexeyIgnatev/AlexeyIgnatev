import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        return None

    def draw_grid(self, screen) -> None:
        for i in range(self.life.cell_height):
            for j in range(self.life.cell_width):
                if self.life.curr_generation[i][j]:
                    screen.addstr(i, j, "*")
        return None

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(False)

        resize = curses.is_term_resized(self.life.cell_height, self.life.cell_width)

        # Action in loop if resize is True:
        if resize is True:
            y, x = screen.getmaxyx()
            screen.clear()
            curses.resizeterm(y, x)
            screen.refresh()

        screen.refresh()

        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            screen.clear()

            self.draw_borders(screen)
            self.draw_grid(screen)

            screen.refresh()

            self.life.step()

        curses.endwin()

        return None


Console(GameOfLife((10, 10))).run()
