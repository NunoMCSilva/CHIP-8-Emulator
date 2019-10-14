# TODO: more like MockScreen, but... check model based testing
class Chip8Screen:
    # 64 x 32 pixels

    def __init__(self, x_size=64, y_size=32, screen_set=None, screen_unset=None):
        self.screen = {}    # TODO: can replaced with set
        self.x_size = x_size
        self.y_size = y_size
        self.screen_set = screen_set
        self.screen_unset = screen_unset

    def cls(self):
        # clear screen
        self.screen = {}

    def get(self, x, y):
        return self.screen.get((x % self.x_size, y % self.y_size), 0)

    def unset(self, x, y):
        self.screen[(x % self.x_size, y % self.y_size)] = 0
        if self.screen_unset is not None:
            self.screen_unset(x, y)

    def set(self, x, y):
        self.screen[(x, y)] = 1
        if self.screen_set is not None:
            self.screen_set(x, y)

    def dump_textshot(self) -> str:
        # a screenshot representation...
        s = ""
        for y in range(self.y_size):
            for x in range(self.x_size):
                s += "X" if self.get(x, y) == 1 else " "
            s += "\n"
        return s
