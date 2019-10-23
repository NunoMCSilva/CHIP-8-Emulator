# TODO: add docstring

import logging

from chip8.keypad import KeyPad
from chip8.memory import Memory
import chip8.opcodes as opcodes
from chip8.screen import Screen

# TODO: recheck
FONT_SET = [
    0xF0, 0x90, 0x90, 0x90, 0xF0,   # 0
    0x20, 0x60, 0x20, 0x20, 0x70,   # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0,   # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0,   # 3
    0x90, 0x90, 0xF0, 0x10, 0x10,   # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0,   # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0,   # 6
    0xF0, 0x10, 0x20, 0x40, 0x40,   # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0,   # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0,   # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90,   # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0,   # B
    0xF0, 0x80, 0x80, 0x80, 0xF0,   # C
    0xE0, 0x90, 0x90, 0x90, 0xE0,   # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0,   # E
    0xF0, 0x80, 0xF0, 0x80, 0x80    # F
]

# TODO: add dict of opcodes = mnemonics

#logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)
# TODO: the opcodes may be used in chip8 tkinter exec window?

#import sys
#from pubsub import pub
#from pubsub.utils.notification import useNotifyByWriteFile
#useNotifyByWriteFile(sys.stdout)

class SimpleInfiniteLoop(Exception):
    pass


class VirtualMachine:

    def __init__(self, program_start: int = 0x200): #, screen_set=None, screen_unset=None):
        # 8-bit memory
        self.memory = Memory()

        # screen
        self.screen = Screen()  #screen_set=screen_set, screen_unset=screen_unset)

        # keypad
        self.keypad = KeyPad()

        # 16-bit program counter
        self.pc = program_start     # todo: consider replacing this by a special byte/bytes class that allows +, >, etc.

        # 8-bit data registers
        self.v = {k: 0x00 for k in range(0xF + 1)}

        # 16-bit address register
        self.i = 0x0000

        # timer registers
        # TODO: decreases at 60Hz, deactivates at ==0
        self.delay_timer_register = 0x00
        # TODO: add works

        # TODO: decreases at 60Hz (once each step), while >0 buzzer will sound (recheck)
        # TODO: only one tone, frequency decided by interpreter
        self.sound_timer_register = 0x00
        # TODO: add works

        # TODO: stack -- It has 16 levels, allowing 16 successive subroutine calls.
        self.stack = []     # TODO: needs beyond max exception

        # load font set
        self.memory.load_data(0x0000, *FONT_SET)

    # TODO: improve all loads and refactor them
    def load_program(self, fpath):
        with open(fpath, "rb") as f:
            self.memory.load_data(0x200, *f.read())     # TODO: might still be improved

    # TODO: refactor
    def run(self, steps=None):
        try:
            while True:
                self.step()
        except SimpleInfiniteLoop:
            pass

    def step(self) -> None:
        # fetch
        opcode = self.memory.get_opcode(self.pc)     # big-endian
        logging.debug(f"{hex(self.pc)} - {hex(opcode)}")

        # parse
        func = self._parse_opcode(opcode)

        # execute
        next_pc = func(*self._add_args(func, opcode))

        if self.pc == next_pc:
            raise SimpleInfiniteLoop

        self.pc = (self.pc + 2) if next_pc is None else next_pc     # TODO: 2 if the usual increment -- put in const?

    # TODO: put in opcodes?
    def _add_args(self, func, opcode):
        for arg in func.__code__.co_varnames[:func.__code__.co_argcount]:
            if arg == "self":
                yield self
            elif arg == "nnn":
                yield opcode & 0x0fff
            elif arg == "nn":
                yield opcode & 0x00ff
            elif arg == "x":
                yield (opcode & 0x0f00) >> 8
            elif arg == "y":
                yield (opcode & 0x00f0) >> 4
            elif arg == "n":
                yield opcode & 0x000f
            else:
                raise NotImplementedError

    """
    def _load_fonts(self):
        # TODO: check if this is correct...
        for i, font_set_element in enumerate(FONT_SET):
            self.memory[i] = font_set_element
    """

    def _parse_opcode(self, opcode):   # (self, opcode: int) -> func
        nibble3 = opcode >> 12

        if nibble3 == 0x0:
            if opcode == 0x00e0:
                return opcodes.opcode_00e0  # TODO: use partial for self?
            elif opcode == 0x00ee:
                return opcodes.opcode_00ee
            else:
                return opcodes.opcode_0nnn
        elif nibble3 == 0x1:
            return opcodes.opcode_1nnn
        elif nibble3 == 0x2:
            return opcodes.opcode_2nnn
        elif nibble3 == 0x3:
            return opcodes.opcode_3nnn
        elif nibble3 == 0x4:
            return opcodes.opcode_4nnn
        elif nibble3 == 0x5:
            nibble0 = opcode & 0x000f

            if nibble0 == 0x0:
                return opcodes.opcode_5xy0
        elif nibble3 == 0x6:
            return opcodes.opcode_6xnn
        elif nibble3 == 0x7:
            return opcodes.opcode_7xnn
        elif nibble3 == 0x8:
            nibble0 = opcode & 0x000f

            if nibble0 == 0x0:
                return opcodes.opcode_8xy0
            elif nibble0 == 0x1:
                return opcodes.opcode_8xy1
            elif nibble0 == 0x2:
                return opcodes.opcode_8xy2
            elif nibble0 == 0x3:
                return opcodes.opcode_8xy3
            elif nibble0 == 0x4:
                return opcodes.opcode_8xy4
            elif nibble0 == 0x5:
                return opcodes.opcode_8xy5
            elif nibble0 == 0x6:
                return opcodes.opcode_8xy6
            elif nibble0 == 0x7:
                return opcodes.opcode_8xy7
            elif nibble0 == 0xE:
                return opcodes.opcode_8xye
        elif nibble3 == 0x9:
            nibble0 = opcode & 0x000f

            if nibble0 == 0x0:
                return opcodes.opcode_9xy0
        elif nibble3 == 0xA:
            return opcodes.opcode_annn
        elif nibble3 == 0xB:
            return opcodes.opcode_bnnn
        elif nibble3 == 0xC:
            return opcodes.opcode_cxnn
        elif nibble3 == 0xD:
            return opcodes.opcode_dxyn
        elif nibble3 == 0xE:
            byte0 = opcode & 0x00ff

            if byte0 == 0x9E:
                return opcodes.opcode_ex9e
            elif byte0 == 0xA1:
                return opcodes.opcode_exa1
        elif nibble3 == 0xF:
            byte0 = opcode & 0x00ff

            if byte0 == 0x07:
                return opcodes.opcode_fx07
            elif byte0 == 0x0A:
                return opcodes.opcode_fx0a
            elif byte0 == 0x15:
                return opcodes.opcode_fx15
            elif byte0 == 0x18:
                return opcodes.opcode_fx18
            elif byte0 == 0x1E:
                return opcodes.opcode_fx1e
            elif byte0 == 0x29:
                return opcodes.opcode_fx29
            elif byte0 == 0x33:
                return opcodes.opcode_fx33
            elif byte0 == 0x55:
                return opcodes.opcode_fx55
            elif byte0 == 0x65:
                return opcodes.opcode_fx65

        raise NotImplementedError(hex(opcode))


if __name__ == "__main__":
    vm = VirtualMachine()
    vm.load_program("tests/integration/data/Chip8 Picture.ch8")     #SQRT Test [Sergey Naydenov, 2010].ch8")
    vm.run()
    vm.screen.get_screenshot().show()
