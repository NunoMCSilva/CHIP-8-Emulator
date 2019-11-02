# TODO: add docstring

# libraries
import logging


# constants
MEMORY_SIZE = 4 * 1024  # 4KiB


# debug
debug = True
if debug:
    logging.basicConfig(level=logging.DEBUG)    # TODO: necessary?


# code
class Memory(bytearray):

    def __init__(self, size: int = MEMORY_SIZE):
        super().__init__(size)

    # TODO: add "pretty print" __str__

    def get_opcode(self, address: int) -> int:
        # get 2 consecutive bytes
        return self[address] << 8 | self[address + 1]

    def load_data(self, start, *args) -> None:
        # load list of bytes to memory
        self[start:start+len(args)] = args
        logging.debug(f"model.vm.memory:{len(args)} byte(s) program loaded to memory")

    # mostly for testing
    def load_opcodes(self, start, *args):
        # load list of opcodes to memory

        # TODO: check if this can be refactored further
        def opcode_to_bytes():
            for opcode in args:
                yield (opcode & 0xff00) >> 8
                yield opcode & 0x00ff

        self.load_data(start, *opcode_to_bytes())

    # TODO: add save, load
