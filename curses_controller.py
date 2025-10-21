import curses
import time


class CursesController:
    def __init__(self, game_logic, ui, input_handler):
        self.game_logic = game_logic
        self.ui = ui
        self.input_handler = input_handler
        self.running = True
        self.paused = False
        self.generation = 0
        self.grid = None

    def setup(self, stdscr, rows: int, cols: int):
        self.stdscr = stdscr
        self.rows = rows
        self.cols = cols

        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(100)

        self.grid = self.game_logic.create_grid(rows, cols)
        self.ui.setup_colors(stdscr)

    def run(self):
        # Главный цикл
        while self.running:
            self.stdscr.clear()

            # Отрисовка
            population_stats = self.game_logic.get_population_stats(self.grid)
            speed_value, speed_name = self.ui.get_current_speed()
            status = 'PAUSED' if self.paused else 'RUNNING'

            self.ui.draw_header(self.stdscr, self.generation, speed_name, status, population_stats)
            self.ui.draw_grid(self.stdscr, self.grid)
            self.stdscr.refresh()

            # Обработка ввода
            key = self.stdscr.getch()
            self._handle_input(key)

            # Обновление игры
            if not self.paused:
                self.grid = self.game_logic.next_generation(self.grid)
                self.generation += 1
                time.sleep(0.05)
            else:
                time.sleep(0.1)

    def _handle_input(self, key):
        # Управление скоростью
        if key in [ord('+'), ord('=')]:
            self.ui.increase_speed()
        elif key in [ord('-'), ord('_')]:
            self.ui.decrease_speed()

        # Паттерны
        self.grid, new_generation = self.input_handler.handle_pattern_key(key, self.grid)
        if new_generation is not None:
            self.generation = new_generation

        # Основные контролы
        action, self.paused, self.generation = self.input_handler.handle_control_key(
            key, self.paused, self.generation
        )

        if action == 'quit':
            self.running = False
        elif action == 'reset':
            self.grid = self.game_logic.create_grid(self.rows, self.cols)
            self.generation = 0
            self.ui.reset_speed()
