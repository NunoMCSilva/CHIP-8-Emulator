# TODO: add docstrings

# libraries
import tkinter as tk

from pubsub import pub


# code
class View(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self._master = master

        self._configure_gui()
        self._create_widgets()
        self._bind_events()

        self._running = False

    def run(self) -> None:
        self.mainloop()

    def _configure_gui(self) -> None:
        self._master.title('CHIP-8 Interpreter')

    def _create_widgets(self) -> None:
        # bottom buttons
        self._buttons = tk.Frame(self._master)
        self._buttons.pack()

        # TODO: have this turned off until load is done
        # TODO: change to stop on click then back
        #self._buttons_play = tk.Button(self._buttons, text="Play", command=self._on_play, state="disabled")
        #self._buttons_play.grid(row=0, column=0)

        #self._buttons_stop = tk.Button(self._buttons, text="Stop", command=self._on_stop, state="disabled")
        #self._buttons_stop.grid(row=0, column=1)

    def _bind_events(self) -> None:
        self._master.bind("<Key>", lambda event: pub.sendMessage("view.keypress", key=event.keysym))

    def _on_step(self) -> None:
        if self._running:
            pub.sendMessage("view.step")
            self.after(1000 // 60,
                       self._on_step)

    """
    # TODO: think correctly what play, pause and stop do (details)
    def _on_play(self) -> None:
        self._running = True
        self._buttons_play.config(text="Pause", command=self._on_pause)
        self.after(0, self._on_step)

    def _on_pause(self) -> None:
        self._running = False
        self._buttons_play.config(text="Play", command=self._on_play)

    def _on_stop(self) -> None:
        self._running = False
        # TODO: change button_play
        # TODO: pub.sendMessage("view.on_stop")
    """


def get_view() -> View:
    root = tk.Tk()
    return View(root)



"""
# libraries
import logging

from tkinter import filedialog




# debug
# TODO: also necessary here?
debug = True
if debug:
    logging.basicConfig(level=logging.DEBUG)




    def __init__(self, master, zoom=10):
        super().__init__(master)


        self._zoom = zoom



        self._pixels = {}   # screen elements in _screen
        self._playing = False  # is it playing?

        # TODO: experimental
        self._waiting_keypress = False
        self._master.bind("<Key>", self._on_keypress)


    def screen_clear(self) -> None:
        # clear screen
        # TODO: verify if it's possible to get this values from tk.Canvas itself
        for x, y in self._pixels:
            self._screen.delete(self._pixels[x, y])
        logging.debug("view.screen.clear()")

    def screen_set(self, x: int, y: int) -> None:
        # set screen pixel
        # TODO: recheck this
        self._pixels[x, y] = self._screen.create_rectangle(
            self._zoom * x, self._zoom * y,
            self._zoom * x + self._zoom, self._zoom * y + self._zoom,
            fill="white", outline="white"
        )

    def screen_unset(self, x: int, y: int) -> None:
        # unset screen pixel
        x = x % 64
        y = y % 32
        self._screen.delete(self._pixels[x, y])
        del self._pixels[x, y]

    def on_model_stop(self) -> None:
        # model has stopped
        self._playing = False

    def on_wait_for_keypress(self) -> None:
        # wait for keypress
        self._playing = False   # TODO: check if need to stop after
        self._waiting_keypress = True
        logging.debug("view.on_wait_for_keypress()")
        # TODO: check event

    def restart(self):
        #self._playing = True
        self._waiting_keypress = False
        self._on_play()

    def _on_keypress(self, event):
        if self._waiting_keypress:
            logging.debug(f"view.on_keypress({event})")
            pub.sendMessage("view.keypress", keypress=event.keysym)
            self._waiting_keypress = False
            # TODO: start self._playing?


    def _create_widgets(self) -> None:
        # TODO: add pause, screenshot, screencast, speed control, zoom control

        # menu
        self._menu = tk.Menu(self._master)
        self._menu.add_command(label="Open...", command=self._on_open)  # TODO: use ... or not on label?
        self._master.config(menu=self._menu)

        # middle screen
        self._screen = tk.Canvas(self._master, width=64 * self._zoom, height=32 * self._zoom, bg="black")
        self._screen.pack()


        self._buttons_step = tk.Button(self._buttons, text="Step", command=lambda: pub.sendMessage("view.step"))
        self._buttons_step.grid(row=0, column=1)

    def _on_open(self) -> None:
        # TODO: improve this
        if not debug:
            fpath = "data/Chip8 Picture.ch8"
        else:
            fpath = filedialog.askopenfilename(
                initialdir="data/",
                title="Select file",
                filetypes=(("chip8_ files", "*.ch8"), ("all files", "*.*")),
            )
        pub.sendMessage("view.open", fpath=fpath)

    def _on_play(self) -> None:
        self._playing = True
        self.after(0, self._on_play_step)

    def _on_play_step(self) -> None:
        if self._playing:
            pub.sendMessage("view.step")
            if self._playing:
                self.after(1000 // 60, self._on_play_step)



"""
