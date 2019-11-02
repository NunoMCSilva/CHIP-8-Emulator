# TODO: add docstrings

# libraries
import logging

from pubsub import pub

from chip8.model.vm import VirtualMachine
from chip8.view import get_view


# debug
debug = True
if debug:
    logging.basicConfig(level=logging.DEBUG)

    #import sys
    #from pubsub.utils.notification import useNotifyByWriteFile
    #useNotifyByWriteFile(sys.stdout)


# code
class Presenter:

    def __init__(self):
        self._model = None
        self._view = get_view()
        self._subscribe_to_listeners()

    def run(self) -> None:
        logging.debug("presenter.run()")
        self._view.run()

    def _subscribe_to_listeners(self) -> None:
        # subscribe to topics from model
        pub.subscribe(self._view.screen_clear, "model.screen.clear")
        pub.subscribe(self._view.screen_set, "model.screen.set")
        pub.subscribe(self._view.screen_unset, "model.screen.unset")
        pub.subscribe(self._view.on_model_stop, "model.stop")
        pub.subscribe(self._view.on_wait_for_keypress, "model.wait_for_keypress")   # TODO: experimental

        # subscribe to topics from view
        pub.subscribe(self._on_view_open, "view.open")
        pub.subscribe(self._on_view_step, "view.step")
        pub.subscribe(self._on_view_keypress, "view.keypress")

    def _on_view_open(self, fpath: str) -> None:
        # init vm with program file
        logging.debug(f"presenter.on_view_open({fpath})")
        self._model = VirtualMachine(program_fpath=fpath)

    def _on_view_step(self) -> None:
        # step 1 instruction (if necessary init vm without program file)
        logging.debug("presenter.on_view_step()")

        # TODO: just use an exception of some sort
        #if self._model is None:
            #self._model = VirtualMachine()

        self._model.step()

    # TODO: hmmm, really need to think about these -- keypress is currently working, but it's an ugly workaround
    def _on_view_keypress(self, keypress):
        # ok, I can put in v[x], but can I find a way of returning that function? -- promises?
        print(keypress)
        x, vx = self._model.on_view_keypress(keypress)
        self._model.change_v(x, vx)
        self._view.restart()
