import curses
from curses_controller import CursesController
from game_logic import create_grid, next_generation, get_population_stats
from input_handler import InputHandler
from ui_components import GameUI


def main(stdscr):
    # Создаем компоненты
    ui = GameUI()
    input_handler = InputHandler(0, 0)

    # Определяем game_logic как объект с методами
    class GameLogic:
        def create_grid(self, rows, cols):
            return create_grid(rows, cols)

        def next_generation(self, grid):
            return next_generation(grid)

        def get_population_stats(self, grid):
            return get_population_stats(grid)

    game_logic = GameLogic()

    # Настраиваем размеры
    max_y, max_x = stdscr.getmaxyx()
    rows, cols = min(20, max_y - 10), min(40, max_x - 2)
    input_handler.rows = rows
    input_handler.cols = cols

    # Создаем и запускаем контроллер
    controller = CursesController(game_logic, ui, input_handler)
    controller.setup(stdscr, rows, cols)
    controller.run()

if __name__ == '__main__':
    curses.wrapper(main)
