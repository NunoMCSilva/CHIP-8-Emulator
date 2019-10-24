import logging
import tkinter as tk
from tkinter import filedialog

from pubsub import pub

logging.basicConfig(level=logging.DEBUG)


# TODO: better logging messages
class View(tk.Frame):

    def __init__(self, master, zoom=10):
        super().__init__(master)
        self._master = master

        self._configure_gui()
        self._create_widgets()
        #self._initialize()

    def run(self):
        self.mainloop()

    def _configure_gui(self):
        self._master.title('CHIP-8 Interpreter')

    def _create_widgets(self):
        # top menu
        self._menu = tk.Menu(self._master)
        self._menu.add_command(label="Open...", command=self._on_open)     # TODO: use ... or not?
        self._master.config(menu=self._menu)

        # middle screen
        self._display = tk.Canvas(self._master, width=640, height=320, bg="black")  # TODO: adjustable zoom
        self._display.pack()

        # bottom buttons
        self._buttons = tk.Frame(self._master)
        self._buttons.pack()

        self._buttons_play = tk.Button(self._buttons, text="Play", command=self._on_play)
        self._buttons_play.grid(row=0, column=0)

        self._buttons_pause = tk.Button(self._buttons, text="Pause", command=self._on_pause)
        self._buttons_pause.grid(row=0, column=1)

        self._buttons_step = tk.Button(self._buttons, text="Step", command=self._on_step)
        self._buttons_step.grid(row=0, column=2)

        self._buttons_stop = tk.Button(self._buttons, text="Stop", command=self._on_stop)
        self._buttons_stop.grid(row=0, column=3)

        self._buttons_screenshot = tk.Button(self._buttons, text="Screenshot", command=self._on_screenshot)
        self._buttons_screenshot.grid(row=0, column=4)

        # TODO: implement this later?
        """
        self._screen_capture_start_button = tk.Button(text="Screen Capture Start")
        self._screen_capture_start_button.pack()

        self._screen_capture_stop_button = tk.Button(text="Screen Capture Start")
        self._screen_capture_stop_button.pack()
        """
        # TODO: add speed adjuster

    # TODO: remove after testing
    def _initialize(self):
        logging.debug("view.initialize")

        fpath = "tests/integration/data/Chip8 Picture.ch8"
        logging.debug(f"view.open:{fpath}")
        pub.sendMessage("view.open", fpath=fpath)

    def _on_open(self):
        logging.debug("view.open")
        fpath = filedialog.askopenfilename(
            initialdir="tests/integration/data/",   # TODO: elsewhere?
            title="Select file",
            filetypes=(("chip8_ files", "*.ch8"), ("all files","*.*"))
        )
        logging.debug(f"view.open:{fpath}")
        pub.sendMessage("view.open", fpath=fpath)

    def _on_play(self):
        logging.debug("view.on_play")
        # TODO: pub.sendMessage("view.play")
        # TODO: self.after(0, self._step)

    def _on_pause(self):
        print("TODO: pause")   # TODO: implement

    def _on_step(self):
        logging.debug("view.on_step")
        pub.sendMessage("view.step")

    def _on_stop(self):
        print("TODO: stop")   # TODO: implement

    def _on_screenshot(self):
        print("TODO: screenshot")   # TODO: implement


def get_view() -> View:
    root = tk.Tk()
    return View(root)



"""
# TODO: add play, stop, pause & speed control
class View(tk.Frame):
        self.zoom = zoom
        self.pixels = {}
        self.stop = False

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
"""
