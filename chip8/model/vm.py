# TODO: add docstring

# libraries
import logging

from pubsub import pub

# TODO: relative imports
from chip8.model.fonts import FONT_SET
from chip8.model.keypad import KeyPad
from chip8.model.memory import Memory
import chip8.model.opcodes as opcodes
from chip8.model.screen import Screen


# constants
PROGRAM_START = 0x200


# debug
debug = True
if debug:
    logging.basicConfig(level=logging.DEBUG)    # TODO: necessary?


# code
class VirtualMachine:
    # TODO: consider replacing all ints with Byte class (allows +, >, __repr__ with hex)

    def __init__(self, program_fpath=None, program_start: int = PROGRAM_START):
        self.program_start = program_start

        # 8-bit memory
        self.memory = Memory()

        # screen
        self.screen = Screen()

        # keypad
        self.keypad = KeyPad()

        # 16-bit program counter
        self.pc = program_start

        # 8-bit data registers
        self.v = {k: 0x00 for k in range(0xF + 1)}

        # 16-bit address register
        self.i = 0x0000

        # TODO: add timer registers, sound registers, audio?

        # TODO: stack -- It has 16 levels, allowing 16 successive subroutine calls.
        self.stack = []     # TODO: needs beyond max exception

        # load font set
        self.memory.load_data(0x0000, *FONT_SET)

        # load program
        if program_fpath is not None:
            self.load_program(program_fpath)

    def load_program(self, fpath: str) -> None:
        logging.debug(f"model.vm:load_program({fpath})")

        with open(fpath, "rb") as f:
            # TODO: might still improve this
            self.memory.load_data(self.program_start, *f.read())

    def step(self) -> None:
        # fetch
        opcode = self.memory.get_opcode(self.pc)     # big-endian

        # parse
        func = opcodes.parse(opcode)

        # execute
        args = tuple(opcodes.add_args(self, func, opcode))
        next_pc = func(*args)

        # debug logging
        if debug:
            logging.debug(f"model.vm:{hex(self.pc)}:{hex(opcode)}:{opcodes.get_mnemonic(func, args)}")

        # check for end of program (usually marked by infinite loop)
        if self.pc == next_pc:
            pub.sendMessage("model.stop")
            #raise StopIteration     # # TODO: raise SimpleInfiniteLoop?

        # increment program counter
        self.pc = (self.pc + 2) if next_pc is None else next_pc     # TODO: 2 if the usual increment -- put in const?

    def on_view_keypress(self, keypress):
        return self.keypad.on_view_keypress(keypress)

    def change_v(self, x, vx):
        self.v[x] = vx
