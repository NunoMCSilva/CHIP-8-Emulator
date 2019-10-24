from pubsub import pub

# TODO: from chip8_.vm import VirtualMachine
from chip8_.vm2 import VirtualMachine
from chip8_.view import get_view


class Presenter:

    def __init__(self):
        self._model = VirtualMachine()
        self._view = get_view()
        self._subscribe_to_listeners()

    def run(self):
        self._view.run()

    def _subscribe_to_listeners(self):
        # subscribe events from model
        pass

        # subscribe events from view
        pub.subscribe(self._model.load_program, "view.open")
        pub.subscribe(self._model.step, "view.step")


"""
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

    ""
    def _on_model_screen_clear(self):
        self._view.clear()

    def _on_model_screen_set(self, x, y):
        self._view.set(x, y)

    def _on_model_screen_unset(self, x, y):
        self._view.unset(x, y)

    def _on_model_infinite_loop(self):
        self._view.infinite_loop()""

    # TODO: add tests to model -- pub.send...
    def _on_view_step(self):
        try:
            self._model.step()
        except SimpleInfiniteLoop:
            print('simple infinite loop')
            pub.sendMessage("model.infinite_loop")

    def run(self):
        self._view.run()
"""
