from patterns import *


class InputHandler:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def handle_pattern_key(self, key, grid):
        new_generation = None

        if key == ord('1'):
            add_glider(grid, self.rows // 2, self.cols // 2)
        elif key == ord('2'):
            add_lightweight_spaceship(grid, self.rows // 2, self.cols // 2)
        elif key == ord('3'):
            add_pulsar(grid, max(0, self.rows // 2 - 6), max(0, self.cols // 2 - 6))
        elif key == ord('4'):
            add_gosper_glider_gun(grid, max(0, self.rows // 2 - 4), max(0, self.cols // 2 - 18))
        elif key == ord('5'):
            add_block(grid, self.rows // 2, self.cols // 2)
        elif key == ord('6'):
            add_blinker(grid, self.rows // 2, self.cols // 2)
        elif key == ord('0'):
            grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        return grid, new_generation

    def handle_control_key(self, key, paused, generation):
        if key == ord('q'):
            return 'quit', paused, generation
        elif key == ord(' '):
            return 'continue', not paused, generation
        elif key == ord('r'):
            return 'reset', False, 0
        return 'continue', paused, generation
