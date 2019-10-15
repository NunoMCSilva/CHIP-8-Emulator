"""
# TODO: add docstrings

import chip8.opcodes as opcodes


class Chip8VirtualMachine:

    def __init__(self, program_start: int = 0x200, memory_size = 4096):
        # 8-bit memory
        self.memory = None  # Chip8Memory(memory_size)

        # 16-bit program counter
        self.pc = program_start

        # 8-bit data registers
        self.v = {k: 0x00 for k in range(0xF + 1)}

        # 16-bit address register
        self.i = 0x0000

        # TODO: add rest

    def step(self) -> None:
        opcode = self._get_opcode()

        self._parse(opcode)

        # TODO: rest

    def _get_opcode(self) -> int:
        return self.memory.get16(self.pc)

    def _parse(self, opcode) -> None:
        nibble3 = opcode >> 12

        # TODO: refactor this
        if nibble3 == 0x0:
            self._parse_0nnn(opcode)
        elif nibble3 == 0x1:
            pass
        elif nibble3 == 0x2:
            pass
        elif nibble3 == 0x3:
            pass
        elif nibble3 == 0x4:
            pass
        elif nibble3 == 0x5:
            pass
        elif nibble3 == 0x6:
            pass
        elif nibble3 == 0x7:
            pass
        elif nibble3 == 0x8:
            pass
        elif nibble3 == 0x9:
            pass
        elif nibble3 == 0xA:
            pass
        elif nibble3 == 0xB:
            pass
        elif nibble3 == 0xC:
            pass
        elif nibble3 == 0xD:
            pass
        elif nibble3 == 0xE:
            pass
        elif nibble3 == 0xF:
            pass

    def _parse_0nnn(self, opcode):
        if opcode == 0x00E0:
            opcodes.opcode_00e0(self)
        elif opcode == 0x00EE:
            opcodes.opcode_00ee(self)
        else:
            nnn=opcode & 0x0fff
            opcodes.opcode_0nnn(self, nnn)
"""


"""
# TODO: this needs a lot of refactoring...
# TODO: add docstring

import functools
import logging
import math
import random

from chip8.memory import Chip8Memory
from chip8.screen import Chip8Screen
#import chip8.op

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
# TODO: the opcodes may be used in chip8 tkinter exec window


# TODO: use partialmethod instead of decorator?
def opcode_parse(func):
    @functools.wraps(func)
    def wrapper(self, opcode):
        var_names = func.__code__.co_varnames[:func.__code__.co_argcount]

        # TODO: refactor this
        func1 = func
        for var_name in var_names:
            if var_name == "self":
                pass
            elif var_name == "x":
                func1 = functools.partial(func1, x=(opcode & 0x0f00) >> 8)
            elif var_name == "y":
                func1 = functools.partial(func1, y=(opcode & 0x00f0) >> 4)
            elif var_name == "n":
                func1 = functools.partial(func1, n=opcode & 0x000f)
            elif var_name == "nn":
                func1 = functools.partial(func1, nn=opcode & 0x00ff)
            elif var_name == "nnn":
                func1 = functools.partial(func1, nnn=opcode & 0x0fff)
            else:
                raise NotImplementedError

        return func1(self)

    return wrapper


def increment_pc(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        value = func(self, *args, **kwargs)  # TODO: recheck this
        self.pc += 2
        return value

    return wrapper


""# TODO: improve this (the self part)
def logging(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        opcode = func.__name__.replace("_", "")
        # TODO: how to do this in a way that access x, y, etc. of opcode?
        return func(self, *args, **kwargs)
    return wrapper
# TODO: add something like this to others (use of @ and dict with all)
# logging.debug(f"{hex(self.pc)} - RND V{hex(x)}, {hex(nn)}")""


class InfiniteLoop(Exception):
    pass


class Chip8VirtualMachine:

    def __init__(self, program_start: int = 0x200, screen_set=None, screen_unset=None):
        # 8-bit memory
        self.memory = Chip8Memory()

        # 16-bit program counter
        self.pc = program_start

        # 8-bit data registers
        self.v = {k: 0x00 for k in range(0xF + 1)}

        # 16-bit address register
        self.i = 0x0000

        # timer registers
        self.delay_timer_register = 0x00    # TODO: check this (8bit) -- decreases at 60Hz, deactivates at ==0
        self.sound_timer_register = 0x00    # TODO: check this (8bit) -- decreases at 60Hz (once each step), while >0 buzzer will sound -- only one tone, frequency decided by interpreter
        # TODO: add timer "works"

        # TODO: stack -- It has 16 levels, allowing 16 successive subroutine calls.
        self.stack = []     # TODO: needs beyond max exception

        # TODO: fonts -- add option not to?
        # TODO: check if this is correct...
        for i, font_set_element in enumerate(FONT_SET):
            self.memory[i] = font_set_element

        # screen
        self.screen = Chip8Screen(screen_set=screen_set, screen_unset=screen_unset)

        # TODO: add keyboard

    def loadf(self, fname):
        def load():
            with open(fname, "rb") as f:
                while True:
                    data = f.read(1)
                    if len(data) == 0:
                        break
                    yield int.from_bytes(data, 'big')

        for pos, byte_ in enumerate(load(), start=0x200):
            # print(hex(pos), byte_)
            self.memory[pos] = byte_

    # TODO: test
    def loadl(self, start, *args):
        # load list of opcodes to memory
        # TODO: refactor
        # TODO: raise in case of out of memory, raise in case of not at start (or add initial_location)
        for add_pos, opcode in enumerate(args):
            byte1, byte0 = (opcode & 0xff00) >> 8, opcode & 0x00ff
            self.memory[start + add_pos * 2] = byte1
            self.memory[start + add_pos * 2 + 1] = byte0

    def run(self, steps=None):
        try:
            while True:
                self.step()
        except InfiniteLoop:
            pass

    def _get_opcode(self) -> int:
        return self.memory.get16(self.pc)   # big-endian

    # TODO: ok, this one needs a lot of refactoring
    def step(self):
        # TODO: refactor
        # TODO: memory obj
        # TODO: maybe parse?

        opcode = self._get_opcode()
        # logging.debug(f"{hex(self.pc)}:{hex(opcode)}")

        # opcode parse
        nibble3 = opcode >> 12
        nibble0 = opcode & 0x000f
        byte0 = opcode & 0x00ff

        if nibble3 == 0x0:
            if opcode == 0x00e0:
                self._00e0()
            elif opcode == 0x00ee:
                self._00ee()
            else:
                self._0nnn(opcode)
        elif nibble3 == 0x1:
            self._1nnn(opcode)
        elif nibble3 == 0x2:
            self._2nnn(opcode)
        elif nibble3 == 0x3:
            self._3xnn(opcode)
        elif nibble3 == 0x4:
            self._4xnn(opcode)
        elif nibble3 == 0x5:
            if nibble0 == 0x0:
                self._5xy0(opcode)
            else:
                raise NotImplementedError(hex(opcode))
        elif nibble3 == 0x6:
            self._6xnn(opcode)
        elif nibble3 == 0x7:
            self._7xnn(opcode)
        elif nibble3 == 0x8:
            if nibble0 == 0x0:
                self._8xy0(opcode)
            elif nibble0 == 0x1:
                self._8xy1(opcode)
            elif nibble0 == 0x2:
                self._8xy2(opcode)
            elif nibble0 == 0x3:
                self._8xy3(opcode)
            elif nibble0 == 0x4:
                self._8xy4(opcode)
            elif nibble0 == 0x5:
                self._8xy5(opcode)
            elif nibble0 == 0x6:
                self._8xy6(opcode)
            elif nibble0 == 0x7:
                self._8xy7(opcode)
            elif nibble0 == 0xe:
                self._8xye(opcode)
            else:
                raise NotImplementedError
        elif nibble3 == 0x9:
            if nibble0 == 0x0:
                self._9xy0(opcode)
            else:
                raise NotImplementedError
        elif nibble3 == 0xa:
            self._annn(opcode)
        elif nibble3 == 0xb:
            self._bnnn(opcode)
        elif nibble3 == 0xc:
            self._cxnn(opcode)
        elif nibble3 == 0xd:
            self._dxyn(opcode)
        elif nibble3 == 0xe:
            if byte0 == 0x9e:
                self._ex9e(opcode)
            elif byte0 == 0xa1:
                self._exa1(opcode)
            else:
                raise NotImplementedError
        elif nibble3 == 0xf:
            if byte0 == 0x07:
                self._fx07(opcode)
            elif byte0 == 0x0a:
                self._fx0a(opcode)
            elif byte0 == 0x15:
                self._fx15(opcode)
            elif byte0 == 0x18:
                self._fx18(opcode)
            elif byte0 == 0x1e:
                self._fx1e(opcode)
            elif byte0 == 0x29:
                self._fx29(opcode)
            elif byte0 == 0x33:
                self._fx33(opcode)
            elif byte0 == 0x55:
                self._fx55(opcode)
            elif byte0 == 0x65:
                self._fx65(opcode)
            else:
                raise NotImplementedError
        else:
            # TODO: better exception
            raise Exception

        return False

    # OpCodes

    # TODO: refactor
    # TODO: add Cowgod's chip-8 tech reference opcodes mnemonic to logging?
    # Assign opcode
    @increment_pc
    @opcode_parse
    def _8xy0(self, x, y):
        # Sets VX to the value of VY.
        self.v[x] = self.v[y]
        # self.pc += 2

    # BCD opcodes -- TODO: check type of bcd
    @opcode_parse
    def _fx33(self, x):
        # Stores the binary-coded decimal representation of VX, with the most significant of three digits at the
        # address in I, the middle digit at I plus 1, and the least significant digit at I plus 2. (In other words,
        # take the decimal representation of VX, place the hundreds digit in memory at location in I, the tens digit
        # at location I+1, and the ones digit at location I+2.)
        dec = self.v[x]

        # TODO: refactor this
        hundreds = math.trunc(dec / 100)
        tens = math.trunc((dec - hundreds * 100) / 10)
        ones = math.trunc(dec - hundreds * 100 - tens * 10)

        # TODO: refactor this
        # TODO: check - natural bcd assumed -- put in constant
        bcd = {0: 0b0000, 1: 0b0001, 2: 0b0010, 3: 0b0011, 4: 0b0100, 5: 0b0101, 6: 0b0110, 7: 0b0111, 8: 0b1000,
               9: 0b1001}
        self.memory[self.i] = bcd[hundreds]
        self.memory[self.i + 1] = bcd[tens]
        self.memory[self.i + 2] = bcd[ones]

        self.pc += 2

    # BitOp opcodes
    @increment_pc
    @opcode_parse
    def _8xy1(self, x, y):
        # Sets VX to VX or VY. (Bitwise OR operation)
        self.v[x] = self.v[x] | self.v[y]
        # self.pc += 2

    @increment_pc
    @opcode_parse
    def _8xy2(self, x, y):
        # Sets VX to VX and VY. (Bitwise AND operation)
        self.v[x] = self.v[x] & self.v[y]
        # self.pc += 2

    @increment_pc
    @opcode_parse
    def _8xy3(self, x, y):
        # Sets VX to VX xor VY.
        self.v[x] = self.v[x] ^ self.v[y]
        # self.pc += 2

    @increment_pc
    @opcode_parse
    def _8xy6(self, x, y):
        # Stores the least significant bit of VX in VF and then shifts VX to the right by 1.
        # TODO: usage of y?
        self.v[0xf] = self.v[x] & 0x01
        self.v[x] = self.v[x] >> 1

    @increment_pc
    @opcode_parse
    def _8xye(self, x, y):
        # Stores the most significant bit of VX in VF and then shifts VX to the left by 1.
        self.v[0xf] = (self.v[x] & 0x80) >> 7
        self.v[x] = (self.v[x] << 1) & 0xff

    # Call opcode
    @opcode_parse
    def _0nnn(self, nnn):
        # Calls RCA 1802 program at address NNN. Not necessary for most ROMs.
        #opcodes.opcode_0nnn(self, nnn)
        raise NotImplementedError

    # Conditional opcodes
    @opcode_parse
    def _3xnn(self, x, nn):
        # Skips the next instruction if VX equals NN. (Usually the next instruction is a jump to skip a code block)
        self.pc += 4 if self.v[x] == nn else 2

    @opcode_parse
    def _4xnn(self, x, nn):
        # Skips the next instruction if VX doesn't equal NN. (Usually the next instruction is a jump to skip a code
        # block)
        self.pc += 4 if self.v[x] != nn else 2

    @opcode_parse
    def _5xy0(self, x, y):
        # Skips the next instruction if VX equals VY. (Usually the next instruction is a jump to skip a code block)
        self.pc += 4 if self.v[x] == self.v[y] else 2

    @opcode_parse
    def _9xy0(self, x, y):
        # Skips the next instruction if VX doesn't equal VY. (Usually the next instruction is a jump to skip a code
        # block)
        self.pc += 4 if self.v[x] != self.v[y] else 2

    # Const opcodes
    # TODO: ok, only works like this... check better
    @increment_pc
    @opcode_parse
    def _6xnn(self, x, nn):
        # Sets VX to NN.
        self.v[x] = nn

    @increment_pc
    @opcode_parse
    def _7xnn(self, x, nn):
        # Adds NN to VX. (Carry flag is not changed)
        self.v[x] = (self.v[x] + nn) & 0xff

    # Display opcodes
    #@logging
    @increment_pc
    @opcode_parse
    def _dxyn(self, x, y, n):
        # Draws a sprite at coordinate (VX, VY) that has a width of 8 pixels and a height of N pixels. Each row of 8
        # pixels is read as bit-coded starting from memory location I; I value doesn’t change after the execution of
        # this instruction. As described above, VF is set to 1 if any screen pixels are flipped from set to unset when
        # the sprite is drawn, and to 0 if that doesn’t happen
        # TODO: refactor
        for y_, add in enumerate(range(n), start=self.v[y]):
            sprite_row = self.memory[self.i + add]

            for x_, i in enumerate(range(7, -1, -1), start=self.v[x]):
                bit = sprite_row // 2 ** i
                sprite_row -= bit * 2 ** i

                pixel = self.screen.get(x_, y_)
                new_pixel = bit ^ pixel

                if pixel == 1:
                    if new_pixel == 1:
                        pass
                    else:
                        self.screen.unset(x_, y_)
                        self.v[0xf] = 0x1  # pixel erased
                else:
                    if new_pixel == 1:
                        self.screen.set(x_, y_)
                    else:
                        pass

    #@logging
    @increment_pc
    def _00e0(self):
        # Clears the screen.
        self.screen.cls()

    # Flow opcodes
    def _00ee(self):
        # Returns from a subroutine.
        self.pc = self.stack.pop()

    # TODO: add precondition: 0x200?
    @opcode_parse
    def _1nnn(self, nnn: int) -> None:
        # Jumps to address NNN.
        if self.pc == nnn:
            raise InfiniteLoop
            #return False    # call to same instruction -- infinite loop (usually used to signal program end)

        self.pc = nnn


    @opcode_parse
    def _2nnn(self, nnn):
        # Calls subroutine at NNN.
        self.stack.append(self.pc)
        self.pc = nnn

    @opcode_parse
    def _bnnn(self, nnn):
        # Jumps to the address NNN plus V0.
        self.pc = nnn + self.v[0x0]

    # KeyOp opcodes
    @opcode_parse
    def _ex9e(self, x):
        # Skips the next instruction if the key stored in VX is pressed. (Usually the next instruction is a jump to
        # skip a code block)
        raise NotImplementedError

    @opcode_parse
    def _exa1(self, x):
        # Skips the next instruction if the key stored in VX isn't pressed. (Usually the next instruction is a jump to
        # skip a code block)
        raise NotImplementedError

    def _fx0a(self, x):
        # A key press is awaited, and then stored in VX. (Blocking Operation. All instruction halted until next key
        # event)
        raise NotImplementedError

    # Math opcodes
    @increment_pc
    @opcode_parse
    def _8xy4(self, x, y):
        # Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't.
        added = self.v[x] + self.v[y]
        self.v[x] = added & 0xff
        self.v[0xf] = added >> 8

    @increment_pc
    @opcode_parse
    def _8xy5(self, x, y):
        # VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
        self.v[0xf] = 0x01 if self.v[x] > self.v[y] else 0x00
        # TODO
        subtracted = self.v[x] - self.v[y]
        if subtracted < 0x00:
            self.v[x] = 0xff + subtracted
        else:
            self.v[x] = subtracted

    # TODO: I would prefer opcode_parse then increment_pc or allow both
    @increment_pc
    @opcode_parse
    def _8xy7(self, x, y):
        # Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
        self.v[0xf] = 0x01 if self.v[y] > self.v[x] else 0x00
        subtracted = self.v[y] - self.v[x]
        if subtracted < 0x00:
            self.v[x] = 0xff + subtracted
        else:
            self.v[x] = subtracted

    # Memory opcodes
    #@logging
    @increment_pc
    @opcode_parse
    def _annn(self, nnn):
        # Sets I to the address NNN.
        self.i = nnn

    @increment_pc
    @opcode_parse
    def _fx1e(self, x):
        # Adds VX to I. VF is set to 1 when there is a range overflow (I+VX>0xFFF), and to 0 when there isn't.
        # This is an undocumented feature of the CHIP-8 and used by the Spacefight 2091! game.
        added = self.i + self.v[x]
        self.i = added
        self.v[0xf] = 0x01 if added > 0xfff else 0x00

    @increment_pc
    @opcode_parse
    def _fx29(self, x):
        # Sets I to the location of the sprite for the character in VX. Characters 0-F (in hexadecimal) are represented
        # by a 4x5 font.
        self.i = self.v[x] * 5

    @increment_pc
    @opcode_parse
    def _fx55(self, x):
        # Stores V0 to VX (including VX) in memory starting at address I. The offset from I is increased by 1 for each
        # value written, but I itself is left unmodified.
        for offset, i in enumerate(range(x + 1), start=self.i):
            self.memory[offset] = self.v[i]

    @increment_pc
    @opcode_parse
    def _fx65(self, x):
        # Fills V0 to VX (including VX) with values from memory starting at address I. The offset from I is increased
        # by 1 for each value written, but I itself is left unmodified.
        for n in range(x + 1):
            self.v[n] = self.memory[self.i + n]

    # Random opcodes
    #@logging
    @increment_pc
    @opcode_parse
    def _cxnn(self, x, nn):
        # Sets VX to the result of a bitwise and operation on a random number (Typically: 0 to 255) and NN.
        self.v[x] = random.randint(0, 255) & nn

    # Sound opcodes
    @increment_pc
    @opcode_parse
    def _fx18(self, x):
        # Sets the sound timer to VX.
        self.sound_timer_register = self.v[x]

    # Timer opcodes
    @increment_pc
    @opcode_parse
    def _fx07(self, x):
        # Sets VX to the value of the delay timer.
        self.v[x] = self.delay_timer_register

    @increment_pc
    @opcode_parse
    def _fx15(self, x):
        # Sets the delay timer to VX.
        self.delay_timer_register = self.v[x]


if __name__ == "__main__":
    vm = Chip8VirtualMachine()
    vm.loadf("Chip8 Picture.ch8")
    vm.run()
    print(vm.screen.dump_textshot())
"""



"""
# TODO: add docstrings




        # TODO: add timer registers
        # TODO: stack
        # TODO: add load font
        # TODO: add screen
        # TODO: add keypad

    def load_program(self, program_fpath: str) -> None:
        pass

    def run(self) -> None:
        pass

    def step(self) -> None:
        opcode = self._get_opcode()

        increment_value = self._parse(opcode)

        self.pc += increment_value

    def _get_opcode(self) -> int:
        return self.memory.get16(self.pc)

    def _parse(self, opcode: int) -> int:
        nibble3 = opcode >> 12

        if nibble3 == 0x0:
            pass
        else:
            raise NotImplementedError

        return 2
"""
