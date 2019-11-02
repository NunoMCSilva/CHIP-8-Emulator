class Memory(bytearray):

    def __init__(self, size: int = 4 * 1024):   # 4KiB
        super().__init__(size)

    # TODO: add better "pretty print"
    def __str__(self):  # TODO: add __repr__?
        s = ""

        # TODO: needs some formatting work
        for address, value in enumerate(self):
            hex_value = hex(value).replace("0x", "")
            if len(hex_value) == 1:
                hex_value = "0" + hex_value
            hex_value = hex_value.upper()

            if address % 0x10 == 0x0:
                # TODO: need same for address
                s += f"{hex(address)}\t{hex_value} "
            elif address % 0x10 == 0xF:
                s += f"{hex_value} \n"
            else:
                s += f"{hex_value} "

        return s

    def get_opcode(self, address: int) -> int:
        # get 2 consecutive bytes
        return self[address] << 8 | self[address + 1]

    def save(self, fpath):
        # TODO: test this
        # save all memory to binary file
        with open(fpath, "wb") as f:
            f.write(self)

    def load(self, fpath):
        # TODO: test this
        # load from binary file to memory
        with open(fpath, "rb") as f:
            data = f.read()
        self.load_data(0x0000, *data)   # TODO: hmmm, self = Memory(f.read())?

    # mostly for testing
    def load_data(self, start, *args) -> None:
        # load list of bytes to memory
        self[start:start+len(args)] = args



if __name__ == "__main__":
    print(Memory())
