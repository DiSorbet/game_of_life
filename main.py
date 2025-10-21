import curses
import time

from game_logic import create_grid, get_population_stats, next_generation
from patterns import *
from ui_components import GameUI
from input_handler import InputHandler


def main(stdscr):
    ui = GameUI()
    ui.setup_colors(stdscr)

    curses.curs_set(0)  # Скрываем курсор
    stdscr.nodelay(1)  # Неблокирующий ввод
    stdscr.timeout(100)

    # Настройка размера
    max_y, max_x = stdscr.getmaxyx()
    rows, cols = min(20, max_y - 10), min(40, max_x - 2)

    # Инициализация игры
    grid = create_grid(rows, cols)
    generation = 0
    speed = 0.1  # initial speed
    paused = False  # pause flag
    input_handler = InputHandler(rows, cols)

    # Главный цикл
    while True:
        stdscr.clear()

        # Отрисовка
        population_stats = get_population_stats(grid)
        speed_value, speed_name = ui.get_current_speed()
        status = 'PAUSED' if paused else 'RUNNING'

        ui.draw_header(stdscr, generation, speed_name, status, population_stats)
        ui.draw_grid(stdscr, grid)
        stdscr.refresh()

        # Обработка ввода
        key = stdscr.getch()

        # Управление
        if key in [ord('+'), ord('=')]:
            ui.increase_speed()
        elif key in [ord('-'), ord('_')]:
            ui.decrease_speed()

        # Паттерны
        grid, new_generation = input_handler.handle_pattern_key(key, grid)
        if new_generation is not None:
            generation = new_generation

        # Основные контролы
        action, paused, generation = input_handler.handle_control_key(key, paused, generation)
        if action == 'quit':
            break
        elif action == 'reset':
            grid = create_grid(rows, cols)
            ui.reset_speed()

        # Обновление игры
        if not paused:
            grid = next_generation(grid)
            generation += 1
            time.sleep(ui.get_current_speed()[0])
        else:
            time.sleep(0.1)


if __name__ == '__main__':
    curses.wrapper(main)
