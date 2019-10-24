# TODO: add docstrings

import logging

from pubsub import pub

from chip8.model.vm import VirtualMachine
from chip8.view import get_view

logging.basicConfig(level=logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------------------
# debug stuff... TODO: remove? work on args flag?
debug = False
if debug:
    import sys
    from pubsub.utils.notification import useNotifyByWriteFile
    useNotifyByWriteFile(sys.stdout)
# ----------------------------------------------------------------------------------------------------------------------


class Presenter:

    def __init__(self):
        self._model = None
        self._view = get_view()
        self._subscribe_to_listeners()

    def run(self) -> None:
        self._view.run()

    def _subscribe_to_listeners(self) -> None:
        # subscribe to topics from model
        pub.subscribe(self._view.screen_clear, "model.screen.clear")
        pub.subscribe(self._view.screen_set, "model.screen.set")
        pub.subscribe(self._view.screen_unset, "model.screen.unset")
        pub.subscribe(self._view.on_model_stop, "model.stop")

        # subscribe to topics from view
        pub.subscribe(self._on_view_open, "view.open")
        pub.subscribe(self._on_view_step, "view.step")

    def _on_view_open(self, fpath: str) -> None:
        self._model = VirtualMachine(program_fpath=fpath)

    def _on_view_step(self) -> None:
        # TODO: add issue with empty model
        self._model.step()
