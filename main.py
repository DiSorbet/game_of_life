import curses
import os
import random
import time


# Создаем поле
def create_grid(rows, cols):
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(1 if random.random() < 0.2 else 0)
        grid.append(row)
    return grid


def count_population(grid):
    return sum(sum(row) for row in grid)


def get_population_stats(grid):
    total_cells = len(grid) * len(grid[0])
    alive = count_population(grid)
    percentage = (alive / total_cells) * 100 if total_cells > 0 else 0
    return alive, total_cells, percentage


# Отрисовываем поле
def print_grid(grid):
    # Преобразуем числа в символы
    for row in grid:
        display_row = []
        for cell in row:
            if cell == 1:
                display_row.append('\033[92m■\033[0m')  # живая клетка
            else:
                display_row.append(' ')  # мертвая клетка
        print('|' + ''.join(display_row) + '|')


# считаем соседей
def count_neighbors(grid, row, col):
    rows = len(grid)  # к-во строк в grid
    cols = len(grid[0])  # к-во столбцов в grid (длина первой строки)
    count = 0

    # Проверяем все 8 соседних клеток
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Пропускаем саму клетку
            if i == 0 and j == 0:
                continue

            # вычисляем координаты соседа
            neighbor_row = (row + i) % rows
            neighbor_col = (col + j) % cols

            # если сосед живой, увеличиваем счетчик
            if grid[neighbor_row][neighbor_col] == 1:
                count += 1
    return count


# next generation
def next_generation(grid):
    # rules
    # 1.Живая клетка с 2-3 соседями выживает, иначе умирает
    # 2. Мертвая клетка с 3 соседями оживает
    rows = len(grid)
    cols = len(grid[0])
    new_grid = create_grid(rows, cols)

    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(grid, i, j)
            if grid[i][j] == 1:
                if neighbors in [2, 3]:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
            else:  # если клетка мертвая
                if neighbors == 3:
                    new_grid[i][j] = 1  # оживает
                else:
                    new_grid[i][j] = 0  # остается мертвой
    return new_grid


def main(stdscr):
    # инициализация цветов
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK),  # живые клетки
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK),  # cтатистика
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # график

    curses.curs_set(0)  # Скрываем курсор
    stdscr.nodelay(1)  # Неблокирующий ввод
    stdscr.timeout(100)

    max_y, max_x = stdscr.getmaxyx()
    rows, cols = min(20, max_y - 8), min(40, max_x - 2)
    grid = create_grid(rows, cols)
    generation = 0
    speed = 0.1  # initial speed
    paused = False  # pause flag

    # для статистики
    max_population = rows * cols

    speed_levels = [
        (0.01, "MAX 🚀"),
        (0.02, "VERY FAST"),
        (0.05, "FAST"),
        (0.1, "NORMAL"),
        (0.2, "SLOW"),
        (0.5, "VERY SLOW"),
        (1.0, "🐢"),
        (2.0, "MAX SLOW")
    ]

    cur_speed_index = 3

    def get_cur_speed():
        return speed_levels[cur_speed_index]

    while True:
        stdscr.clear()

        # Статистика населения
        alive, total, percentage = get_population_stats(grid)

        # Заголовок и стстистика
        status = 'PAUSED' if paused else 'RUNNING'
        cur_speed_value, cur_speed_name = get_cur_speed()

        stdscr.addstr(0, 0, f"🎮 GAME OF LIFE | Gen: {generation} | Speed: {cur_speed_name}| Status {status}")
        stdscr.addstr(1, 0, f"🧬 POPULATION: {alive}/{total} ({percentage:.1f}%)", curses.color_pair(2))
        stdscr.addstr(2, 0, f"Controls: [q]uit, [SPACE]pause,[+]faster, [-]slower, [r]eset")

        # Рисуем поле
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    stdscr.addstr(i + 3, j * 2, "██", curses.color_pair(1))
                else:
                    stdscr.addstr(i + 3, j * 2, "  ")
        stdscr.refresh()

        # Обработка клавиш
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord(' '):  # Пробел - пауза/продолжить
            paused = not paused
        elif key == ord('+') or key == ord('='):  # увеличить скорость
            cur_speed_index = max(0, cur_speed_index - 1)
        elif key == ord('_') or key == ord('-'):
            cur_speed_index = min(len(speed_levels) - 1, cur_speed_index + 1)
        elif key == ord('r'):
            grid = create_grid(rows, cols)
            generation = 0
            cur_speed_index = 3
            paused = False

        # Обновляем поколение, если не на паузе
        if not paused:
            grid = next_generation(grid)
            generation += 1
            time.sleep(cur_speed_value)
        else:
            # Если на паузе, небольшая задержка чтобы не грузить процессор
            time.sleep(0.1)


if __name__ == '__main__':
    curses.wrapper(main)
