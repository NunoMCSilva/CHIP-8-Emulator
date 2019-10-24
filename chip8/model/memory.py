# TODO: add docstring

import logging

MEMORY_SIZE = 4 * 1024  # 4KiB

logging.basicConfig(level=logging.DEBUG)


class Memory(bytearray):

    def __init__(self, size: int = MEMORY_SIZE):   # 4KiB
        super().__init__(size)

    # TODO: add "pretty print" __str__

    def get_opcode(self, address: int) -> int:
        # get 2 consecutive bytes
        return self[address] << 8 | self[address + 1]

    def load_data(self, start, *args) -> None:
        # load list of bytes to memory
        self[start:start+len(args)] = args
        logging.debug(f"model:vm:memory:{len(args)} byte(s) program loaded to memory")

    # TODO: add save, load, load_opcodes
