# TODO: add docstring

# libraries
# TODO: add screenshot PIL

from pubsub import pub


# constants
WIDTH = 64
HEIGHT = 32


# code
class Screen:

    def __init__(self, width=WIDTH, height=HEIGHT):
        self.screen = {}
        self.width = width
        self.height = height

    def clear(self):
        # clear screen
        self.screen = {}
        pub.sendMessage("model.screen.clear")

    def get(self, x, y):
        return self.screen.get((x % self.width, y % self.height), 0)

    def set(self, x, y):
        self.screen[(x, y)] = 1
        pub.sendMessage("model.screen.set", x=x, y=y)

    def unset(self, x, y):
        self.screen[(x % self.width, y % self.height)] = 0
        pub.sendMessage("model.screen.unset", x=x, y=y)

    # TODO: add get screenshot
