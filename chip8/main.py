import tkinter as tk

from chip8.vm import Chip8VirtualMachine, InfiniteLoop


class App(tk.Frame):

    def __init__(self, master):
        self._master = master
        super().__init__(self._master)

        self._configure_gui()
        self._create_widgets()

        # TODO: experimental
        self.vm = Chip8VirtualMachine(screen_set=self._set, screen_unset=self._unset)   # TODO: needs better

        # self.vm.loadf("Chip8 Picture.ch8")
        # self.vm.loadf("IBM Logo.ch8")

        # TODO: check error on this one
        # self.vm.loadf("Chip8 emulator Logo [Garstyciuks].ch8")

        # TODO: need to implement wait for key
        # self.vm.loadf("Chip-8 Pack/Chip-8 Programs/Random Number Test [Matthew Mikolay, 2010].ch8")

        # TODO: check error no screen instructions
        # self.vm.loadf("Chip-8 Pack/Chip-8 Programs/Division Test [Sergey Naydenov, 2010].ch8")

        # TODO: check error no screen instructions
        # self.vm.loadf("Chip-8 Pack/Chip-8 Programs/SQRT Test [Sergey Naydenov, 2010].ch8")

        self.vm.loadf("../resources/Chip-8 Pack/Chip-8 Demos/Maze [David Winter, 199x].ch8")
        # TODO: add this to tests (store rnd instructs)...

        #self.vm.loadf("Chip-8 Pack/Chip-8 Demos/Maze (alt) [David Winter, 199x].ch8")

        # TOdO: add this to tests -- needs a screen model with gui -- takes a bit to create
        #self.vm.loadf("Chip-8 Pack/Chip-8 Demos/Sirpinski [Sergey Naydenov, 2010].ch8")

        # TODO: yup, nowhere near able to run this one
        #self.vm.loadf("Chip-8 Pack/Chip-8 Demos/Trip8 Demo (2008) [Revival Studios].ch8")

        #self.vm.loadf("Chip-8 Pack/Chip-8 Demos/Zero Demo [zeroZshadow, 2007].ch8")

        #self.vm.loadf("Chip-8 Pack/Chip-8 Games/15 Puzzle [Roger Ivie] (alt).ch8")  # TODO: check error -- run all by david winter's emul first

        # self.vm.loadf("Chip-8 Pack/Chip-8 Games/Airplane.ch8") -- TODO: check erorr

        self.after(0, self._step)

    def _configure_gui(self):
        self._master.title('CHIP-8 Interpreter')

    def _create_widgets(self):
        self._display = tk.Canvas(self._master, width=640, height=320, bg='black')  # 10x zoom
        self._display.pack()

    def _step(self):
        try:
            self.vm.step()
            self.after(1000 // 60, self._step)   # ~60Hz
            # TODO: add speed button
            #self.after(1000 // 600, self._step)  # ~600Hz -- 10x faster
            #self.after(1000 // (600 * 2), self._step)  # ~1200Hz -- 20x faster -- TODO: too fast
        except InfiniteLoop:
            pass

    def _set(self, x, y):
        x = 10*x
        y = 10*y
        self._display.create_rectangle(x, y, x + 10, y + 10, fill='white')

    def _unset(self, x, y):
        # TODO: would be better to remove the rectangle, but good enough for testing...
        x = 10*x
        y = 10*y
        self._display.create_rectangle(x, y, x + 10, y + 10, fill='black')


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
