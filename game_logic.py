import random


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
