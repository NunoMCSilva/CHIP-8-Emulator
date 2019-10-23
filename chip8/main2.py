# cleaner MVP-FP version (Model-View-Presenter Presenter-First)
# TODO: verify code, separate view?

import tkinter as tk

from pubsub import pub

from chip8.vm import VirtualMachine, SimpleInfiniteLoop


# TODO: add play, stop, pause & speed control
class View(tk.Frame):

    def __init__(self, master, zoom=10):
        self._master = master
        super().__init__(master)

        self._configure_gui()
        self._create_widgets()

        self.zoom = zoom
        self.pixels = {}
        self.stop = False

    def _configure_gui(self):
        self._master.title('CHIP-8 Interpreter')

    def _create_widgets(self):
        self._display = tk.Canvas(self._master, width=640, height=320, bg="black")
        self._display.pack()

    def _step(self):
        pub.sendMessage("view.step")
        if not self.stop:
            self.after(1000 // 60, self._step)

    def run(self):
        self.after(0, self._step)
        self.mainloop()

    def clear(self):
        #self._display.clear()
        pass

    def set(self, x, y):
        self.pixels[x, y] = self._display.create_rectangle(
            self.zoom * x, self.zoom * y,
            self.zoom * x + self.zoom, self.zoom * y + self.zoom,
            fill="white", outline="white"
        )

    def unset(self, x, y):
        self._display.delete(self.pixels[x, y])
        del self.pixels[x, y]

    def infinite_loop(self):
        self.stop = True


class Presenter:

    def __init__(self):
        # model
        self._model = VirtualMachine()
        self._model.load_program("/home/blackcat/Documentos/Projects/Programming/Miscellaneous/CHIP-8 Interpreter/Chip8/tests/integration/data/Chip8 Picture.ch8")

        # view
        self._root = tk.Tk()    # TODO: necessary?
        self._view = View(self._root)

        # subscribe events from model
        #pub.subscribe(self._on_model_screen_clear, "model.screen.clear")
        pub.subscribe(self._view.clear, "model.screen.clear")
        #pub.subscribe(self._on_model_screen_set, "model.screen.set")
        pub.subscribe(self._view.set, "model.screen.set")
        #pub.subscribe(self._on_model_screen_unset, "model.screen.unset")
        pub.subscribe(self._view.unset, "model.screen.unset")
        #pub.subscribe(self._on_model_infinite_loop, "model.infinite_loop")
        pub.subscribe(self._view.infinite_loop, "model.infinite_loop")

        # subscribe events from view
        pub.subscribe(self._on_view_step, "view.step")

    """
    def _on_model_screen_clear(self):
        self._view.clear()

    def _on_model_screen_set(self, x, y):
        self._view.set(x, y)

    def _on_model_screen_unset(self, x, y):
        self._view.unset(x, y)

    def _on_model_infinite_loop(self):
        self._view.infinite_loop()"""

    # TODO: add tests to model -- pub.send...
    def _on_view_step(self):
        try:
            self._model.step()
        except SimpleInfiniteLoop:
            print('simple infinite loop')
            pub.sendMessage("model.infinite_loop")

    def run(self):
        self._view.run()


if __name__ == "__main__":
    Presenter().run()
