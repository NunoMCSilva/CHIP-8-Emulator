# TODO: add docstring

import logging
import tkinter as tk
from tkinter import filedialog

from pubsub import pub

logging.basicConfig(level=logging.DEBUG)


class View(tk.Frame):

    def __init__(self, master, zoom=10):
        super().__init__(master)

        self._master = master
        self._zoom = zoom
        self._pixels = {}

        self._configure_gui()
        self._create_widgets()

    def screen_clear(self):
        for x, y in self._pixels:
            self._screen.delete(self._pixels[x, y])
        self._pixels = {}

    def screen_set(self, x, y):
        # TODO: recheck this
        self._pixels[x, y] = self._screen.create_rectangle(
            self._zoom * x, self._zoom * y,
            self._zoom * x + self._zoom, self._zoom * y + self._zoom,
            fill="white", outline="white"
        )

    def screen_unset(self, x, y):
        self._screen.delete(self._pixels[x, y])
        del self._pixels[x, y]

    def on_model_stop(self):
        raise NotImplementedError

    def run(self):
        self.mainloop()

    def _configure_gui(self):
        self._master.title('CHIP-8 Interpreter')

    def _create_widgets(self):
        # TODO: add pause, screenshot, screencast, speed control, zoom control

        # menu
        self._menu = tk.Menu(self._master)
        self._menu.add_command(label="Open...", command=self._on_open)  # TODO: use ... or not on label?
        self._master.config(menu=self._menu)

        # middle screen
        # TODO: adjustable zoom
        self._screen = tk.Canvas(self._master, width=64 * self._zoom, height=32 * self._zoom, bg="black")
        self._screen.pack()

        # bottom buttons
        self._buttons = tk.Frame(self._master)
        self._buttons.pack()

        # TODO: change to stop on click
        self._buttons_play = tk.Button(self._buttons, text="Play", command=self._on_play)
        self._buttons_play.grid(row=0, column=0)

        self._buttons_step = tk.Button(self._buttons, text="Step", command=self._on_step)
        self._buttons_step.grid(row=0, column=2)

    def _on_open(self):
        fpath =  "data/Chip8 Picture.ch8"
        # TODO: put filedialog again after testing
        """
        fpath = filedialog.askopenfilename(
            initialdir="data/",
            title="Select file",
            filetypes=(("chip8_ files", "*.ch8"), ("all files", "*.*")),
        )
        """
        logging.debug(f"view:filedialog.askopenfilename -> {fpath}")    # TODO: improve logging msgs
        pub.sendMessage("view.open", fpath=fpath)

    def _on_play(self):
        pass

    def _on_step(self):
        pub.sendMessage("view.step")


def get_view() -> View:
    root = tk.Tk()
    return View(root)
