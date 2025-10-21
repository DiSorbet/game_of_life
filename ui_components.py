import curses


class GameUI:
    def __init__(self):
        self.speed_levels = [
            (0.01, "MAX 🚀"),
            (0.02, "VERY FAST"),
            (0.05, "FAST"),
            (0.1, "NORMAL"),
            (0.2, "SLOW"),
            (0.5, "VERY SLOW"),
            (1.0, "🐢"),
            (2.0, "MAX SLOW")
        ]
        self.cur_speed_index = 3

    def setup_colors(self, stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # живые клетки
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # cтатистика
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # график

    def draw_header(self, stdscr, generation, speed_name, status, population_stats):
        alive, total, percentage = population_stats
        stdscr.addstr(0, 0, f"🎮 GAME OF LIFE | Gen: {generation} | Speed: {speed_name}| Status {status}")
        stdscr.addstr(1, 0, f"🧬 POPULATION: {alive}/{total} ({percentage:.1f}%)", curses.color_pair(2))
        stdscr.addstr(2, 0, f"Controls: [q]uit, [SPACE]pause,[+]faster, [-]slower, [r]eset, [0]clear")
        stdscr.addstr(3, 0, "🔧 PATTERNS: [1]glider [2]spaceship [3]pulsar [4]glider gun")
        stdscr.addstr(4, 0, "           [5]block [6]blinker")

    def draw_grid(self, stdscr, grid):
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    stdscr.addstr(i + 6, j * 2, "██", curses.color_pair(1))
                else:
                    stdscr.addstr(i + 6, j * 2, "  ")

    def get_current_speed(self):
        return self.speed_levels[self.cur_speed_index]

    def increase_speed(self):
        self.cur_speed_index = max(0, self.cur_speed_index - 1)

    def decrease_speed(self):
        self.cur_speed_index = min(len(self.speed_levels) - 1, self.cur_speed_index + 1)

    def reset_speed(self):
        self.cur_speed_index = 3
