class Memory:
    # 8-byte RAM

    def __init__(self, size: int = 4096):   # 4KiB
        self.memory = {}
        self.size = size

    def __getitem__(self, address: int) -> int:
        # TODO: add out of memory exception
        return self.memory.get(address, 0x00)

    def __setitem__(self, address, value):
        # TODO: add out of memory exception
        self.memory[address] = value

    def get16(self, address: int) -> int:
        # get 2 consecutive bytes
        return self[address] << 8 | self[address + 1]

    def load_data(self, start, *args):
        # load list of bytes to memory
        # TODO: refactor
        # TODO: raise in case of out of memory, raise in case of not at start (or add initial_location)
        for pos, byte_ in enumerate(args, start=start):
            self.memory[pos] = byte_

    def load_opcodes(self, start, *args):
        # load list of opcodes to memory
        # TODO: refactor
        # TODO: raise in case of out of memory, raise in case of not at start (or add initial_location)
        for add_pos, opcode in enumerate(args):
            byte1, byte0 = (opcode & 0xff00) >> 8, opcode & 0x00ff
            self.memory[start + add_pos * 2] = byte1
            self.memory[start + add_pos * 2 + 1] = byte0
