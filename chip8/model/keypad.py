# TODO: add docstring

class KeyPad:
    # 1-F hexadecimal layout (map to keyboard)

    # TODO: load keyboard map?

    def wait_for_keypress(self) -> int:
        # halting instruction
        raise NotImplementedError

    def is_this_key_pressed(self, key) -> bool:
        raise NotImplementedError
