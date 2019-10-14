class Chip8Memory:
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

    # TODO: load
