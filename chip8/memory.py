class Memory(bytearray):

    def __init__(self, size: int = 4 * 1024):   # 4KiB
        super().__init__(size)

    def get_opcode(self, address: int) -> int:
        # get 2 consecutive bytes
        return self[address] << 8 | self[address + 1]

    def load_data(self, start, *args):
        # load list of bytes to memory
        # TODO: refactor
        for address, value in enumerate(args, start=start):
            self[address] = value

    def load_opcodes(self, start, *args):
        # load list of opcodes to memory
        # TODO: refactor
        for add_address, opcode in enumerate(args):
            byte1, byte0 = (opcode & 0xff00) >> 8, opcode & 0x00ff
            self[start + add_address * 2] = byte1
            self[start + add_address * 2 + 1] = byte0
