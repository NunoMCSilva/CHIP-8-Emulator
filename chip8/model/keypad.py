# TODO: add docstrings

# libraries
from pubsub import pub


# code
# TODO: I'm starting to think my approach to keypad is completely wrong and those opcodes need to not be executed, and instead...
class KeyPad:
    # 1-F hexadecimal layout (map to keyboard)

    # TODO: load keyboard map?
    def __init__(self):
        self.x = None

    # TODO: consider async, await usage
    # TODO: the issue with this seems to be the issue with "the mid step pause" in step -- check that
    def wait_for_keypress(self) -> int:
        # halting instruction
        pub.sendMessage("model.wait_for_keypress")
        return None     # TODO: trying workaround

        #import threading
        #event = threading.Event()
           # this pauses the system
        #print(event)
        #event.wait()    # stops where (stops gui as well) -- would need to run in a diferent thread

        # TODO: check how to work with this in case of VM only
        # ok, pauses system, then wait, then pub.sendMess is down to model, and then... how to return from wait_from_keypress?
        # multithreading would work? -- maybe a producer/consumer
        # pub.sendMessage a Queue and when pub.send from the other side it fills it and exists this funct... need a small case...
        # considering wait -- mainloop

    def wait_for_keypress1(self, x) -> None:
        self.x = x
        pub.sendMessage("model.wait_for_keypress")

    def on_view_keypress(self, keypress):
        x = self.x
        self.x = None
        return x, 0x05

    # TODO: this one might be easier, since it's just view.on_key_press to model and model storing it for 1 step and it erased every step
    def is_this_key_pressed(self, key) -> bool:
        raise NotImplementedError
