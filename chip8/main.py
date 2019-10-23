import tkinter as tk

from chip8.vm import VirtualMachine, SimpleInfiniteLoop
from chip8.screen import Screen


class GuiScreen(tk.Canvas):
    zoom = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = None
        self.pixels = {}

    def surround(self, screen):
        self.screen = screen
        return self

    def clear(self):
        #print("clear")
        self.screen.clear()

    def get(self, x, y):
        #print(f"get {x} {y}")
        return self.screen.get(x, y)

    def set(self, x, y):
        #print(f"set {x} {y}")

        # TODO: recheck this
        self.pixels[x, y] = self.create_rectangle(
            self.zoom * x, self.zoom * y,
            self.zoom * x + self.zoom, self.zoom * y + self.zoom,
            fill="white", outline="white"
        )
        self.screen.set(x, y)

    def unset(self, x, y):
        #print(f"unset {x} {y}")

        # TODO: recheck this
        self.delete(self.pixels[x, y])
        del self.pixels[x, y]

        self.screen.unset(x, y)


class App(tk.Frame):

    def __init__(self, master):
        self._master = master
        super().__init__(self._master)

        self._configure_gui()
        self._create_widgets()

        self._initialize()

    def _configure_gui(self):
        self._master.title('CHIP-8 Interpreter')

    def _create_widgets(self):
        self._display = GuiScreen(self._master, width=640, height=320, bg='black')
        self._display.pack()

    def _initialize(self):
        # program = "tests/integration/data/Chip8 Picture.ch8"
        # program = "tests/integration/data/Random Number Test [Matthew Mikolay, 2010].ch8"   # TODO: wait for keypress

        # TODO: glitchy and never ends?
        # program = "tests/integration/data/SQRT Test [Sergey Naydenov, 2010].ch8"

        program = "tests/integration/data/Chip-8 Pack/Chip-8 Demos/Maze (alt) [David Winter, 199x].ch8"

        self.vm = VirtualMachine()
        self.vm.load_program(program)
        self.vm.screen = self._display.surround(self.vm.screen)

        self.after(0, self._step)

    def _step(self):
        try:
            self.vm.step()
            self.after(1000 // 60, self._step)   # ~60Hz    # TODO: add speed control
        except SimpleInfiniteLoop:
            pass


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()




"""# self.vm.loadf("IBM Logo.ch8")

        # TODO: check error on this one
        # self.vm.loadf("Chip8 emulator Logo [Garstyciuks].ch8")

        # TODO: need to implement wait for key
        # self.vm.loadf("Chip-8 Pack/Chip-8 Programs/Random Number Test [Matthew Mikolay, 2010].ch8")

        # TODO: check error no screen instructions
        # self.vm.loadf("Chip-8 Pack/Chip-8 Programs/Division Test [Sergey Naydenov, 2010].ch8")

        # TODO: check error no screen instructions
        # self.vm.loadf("Chip-8 Pack/Chip-8 Programs/SQRT Test [Sergey Naydenov, 2010].ch8")

        self.vm.load_program("Chip-8 Pack/Chip-8 Demos/Maze [David Winter, 199x].ch8")
        # TODO: add this to tests (store rnd instructs)...

        #self.vm.loadf("Chip-8 Pack/Chip-8 Demos/Maze (alt) [David Winter, 199x].ch8")

        # TOdO: add this to tests -- needs a screen model with gui -- takes a bit to create
        #self.vm.loadf("Chip-8 Pack/Chip-8 Demos/Sirpinski [Sergey Naydenov, 2010].ch8")

        # TODO: yup, nowhere near able to run this one
        #self.vm.loadf("Chip-8 Pack/Chip-8 Demos/Trip8 Demo (2008) [Revival Studios].ch8")

        #self.vm.loadf("Chip-8 Pack/Chip-8 Demos/Zero Demo [zeroZshadow, 2007].ch8")

        #self.vm.loadf("Chip-8 Pack/Chip-8 Games/15 Puzzle [Roger Ivie] (alt).ch8")  # TODO: check error -- run all by david winter's emul first

        # self.vm.loadf("Chip-8 Pack/Chip-8 Games/Airplane.ch8") -- TODO: check erorr

        #self.vm.loadf("BMP Viewer - Hello (C8 example) [Hap, 2005].ch8") -- TODO: no work""

        

    def _set(self, x, y):
        x = 10*x
        y = 10*y
        self._display.create_rectangle(x, y, x + 10, y + 10, fill='white')

    def _unset(self, x, y):
        # TODO: would be better to remove the rectangle, but good enough for testing...
        x = 10*x
        y = 10*y
        self._display.create_rectangle(x, y, x + 10, y + 10, fill='black')"""


