# TODO: add docstrings
# TODO: is hypothesis useful here?

# opcodes put here to facilitate dev
# docstrings taken from mmttmik : Mastering CHIP-8 -- TODO: add thanks
# TODO: instead of int can I use more specific typing?


# libraries
import math
import random
#from typing import Callable


# code
def parse(opcode: int): # -> Callable:
    # parses opcode and returns appropriate function

    nibble3 = opcode >> 12

    # TODO: improve this
    if nibble3 == 0x0:
        if opcode == 0x00e0:
            return opcode_00e0  # TODO: use partial for self?
        elif opcode == 0x00ee:
            return opcode_00ee
        else:
            return opcode_0nnn
    elif nibble3 == 0x1:
        return opcode_1nnn
    elif nibble3 == 0x2:
        return opcode_2nnn
    elif nibble3 == 0x3:
        return opcode_3nnn
    elif nibble3 == 0x4:
        return opcode_4nnn
    elif nibble3 == 0x5:
        nibble0 = opcode & 0x000f

        if nibble0 == 0x0:
            return opcode_5xy0
    elif nibble3 == 0x6:
        return opcode_6xnn
    elif nibble3 == 0x7:
        return opcode_7xnn
    elif nibble3 == 0x8:
        nibble0 = opcode & 0x000f

        if nibble0 == 0x0:
            return opcode_8xy0
        elif nibble0 == 0x1:
            return opcode_8xy1
        elif nibble0 == 0x2:
            return opcode_8xy2
        elif nibble0 == 0x3:
            return opcode_8xy3
        elif nibble0 == 0x4:
            return opcode_8xy4
        elif nibble0 == 0x5:
            return opcode_8xy5
        elif nibble0 == 0x6:
            return opcode_8xy6
        elif nibble0 == 0x7:
            return opcode_8xy7
        elif nibble0 == 0xE:
            return opcode_8xye
    elif nibble3 == 0x9:
        nibble0 = opcode & 0x000f

        if nibble0 == 0x0:
            return opcode_9xy0
    elif nibble3 == 0xA:
        return opcode_annn
    elif nibble3 == 0xB:
        return opcode_bnnn
    elif nibble3 == 0xC:
        return opcode_cxnn
    elif nibble3 == 0xD:
        return opcode_dxyn
    elif nibble3 == 0xE:
        byte0 = opcode & 0x00ff

        if byte0 == 0x9E:
            return opcode_ex9e
        elif byte0 == 0xA1:
            return opcode_exa1
    elif nibble3 == 0xF:
        byte0 = opcode & 0x00ff

        if byte0 == 0x07:
            return opcode_fx07
        elif byte0 == 0x0A:
            return opcode_fx0a
        elif byte0 == 0x15:
            return opcode_fx15
        elif byte0 == 0x18:
            return opcode_fx18
        elif byte0 == 0x1E:
            return opcode_fx1e
        elif byte0 == 0x29:
            return opcode_fx29
        elif byte0 == 0x33:
            return opcode_fx33
        elif byte0 == 0x55:
            return opcode_fx55
        elif byte0 == 0x65:
            return opcode_fx65

    raise NotImplementedError(hex(opcode))


def add_args(self, func, opcode):
    # TODO: needs some work
    # checks function and generates necessary args

    # TODO: put this in opcodes?
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


def get_mnemonic(func, args):
    # experimental mnemonic (for debug logging)
    # TODO: args -- convert to hex already...
    # TODO: needs work
    ops = {
        # TODO: better opcodes -- check cowgod?

        opcode_0nnn: lambda _, nnn: f"SYS {nnn}",
        opcode_00e0: lambda _: f"CLS",
        opcode_00ee: lambda _: f"RET",
        opcode_1nnn: lambda _, nnn: f"JP {nnn}",
        opcode_2nnn: lambda _, nnn: f"call {nnn}",
        opcode_3nnn: lambda _, x, nn: f"SE V{x}, {nn}",
        opcode_4nnn: lambda _, x, nn: f"SNE V{x}, {nn}",
        opcode_5xy0: lambda _, x, y: f"SE V{x}, V{y}",
        opcode_6xnn: lambda _, x, nn: f"LD V{x}, {nn}",
        opcode_7xnn: lambda _, x, nn: f"ADD V{x}, {nn}",
        opcode_8xy0: lambda _, x, y: f"LD V{x}, V{y}",
        opcode_8xy1: lambda _, x, y: f"OR V{x}, V{y}",
        opcode_8xy2: lambda _, x, y: f"AND V{x}, V{y}",
        opcode_8xy3: lambda _, x, y: f"XOR V{x}, V{y}",
        opcode_8xy4: lambda _, x, y: f"ADD V{x}, V{y}",
        opcode_8xy5: lambda _, x, y: f"SUB V{x}, V{y}",
        opcode_8xy6: lambda _, x, y: f"SHR V{x}, V{y}",
        opcode_8xy7: lambda _, x, y: f"SUBN V{x}, V{y}",
        opcode_8xye: lambda _, x, y: f"SHL V{x}, V{y}",
        opcode_9xy0: lambda _, x, y: f"SNE V{x}, V{y}",
        opcode_annn: lambda _, nnn: f"LD I, {nnn}",
        opcode_bnnn: lambda _, nnn: f"JP V0, {nnn}",
        opcode_cxnn: lambda _, x, nn: f"RND V{x}, {nn}",
        opcode_dxyn: lambda _, x, y, n: f"DRW V{x}, V{y}, {n}",
        opcode_ex9e: lambda _, x: f"SKP V{x}",
        opcode_exa1: lambda _, x: f"SKNP V{x}",
        opcode_fx07: lambda _, x: f"LD V{x}, DT",
        opcode_fx0a: lambda _, x: f"LD V{x}, K",
        opcode_fx15: lambda _, x: f"LD DT, V{x}",
        opcode_fx18: lambda _, x: f"LD ST, V{x}",
        opcode_fx1e: lambda _, x: f"ADD I, V{x}",
        opcode_fx29: lambda _, x: f"LD F, V{x}",
        opcode_fx33: lambda _, x: f"LD B, V{x}",
        opcode_fx55: lambda _, x: f"LD [I], V{x}",
        opcode_fx65: lambda _, x: f"LD Vx, [i]",
    }

    # TODO: check diff param, args
    # hex it
    new_args = []
    for arg, param in zip(func.__code__.co_varnames[:func.__code__.co_argcount], args):
        if arg != "self":
            param = hex(param)
        new_args.append(param)

    return ops[func](*new_args)  # TODO: two *, check performance


# code -- opcodes
def opcode_0nnn(self, nnn) -> None:
    """0NNN Execute machine language subroutine at address NNN"""
    raise NotImplementedError


def opcode_00e0(self) -> None:
    """00E0	Clear the screen"""
    self.screen.clear()


def opcode_00ee(self) -> int:
    """00EE	Return from a subroutine"""
    return self.stack.pop() + 2
    # TODO: will needs 16max limit and test


def opcode_1nnn(self, nnn) -> int:
    """1NNN Jump to address NNN"""
    # TODO: detect SimpleInfiniteLoop? (usually to signal program end)? -- needs test
    return nnn


def opcode_2nnn(self, nnn) -> int:
    """2NNN Execute subroutine starting at address NNN"""
    self.stack.append(self.pc)    # TODO: will needs 16max limit and test
    return nnn


def opcode_3nnn(self, x, nn) -> int:
    """3XNN Skip the following instruction if the value of register VX equals NN"""
    return self.pc + (4 if self.v[x] == nn else 2)


def opcode_4nnn(self, x, nn) -> int:
    """4XNN Skip the following instruction if the value of register VX is not equal to NN"""
    return self.pc + (4 if self.v[x] != nn else 2)


def opcode_5xy0(self, x, y) -> int:
    """5XY0 Skip the following instruction if the value of register VX is equal to the value of register VY"""
    return self.pc + (4 if self.v[x] == self.v[y] else 2)


def opcode_6xnn(self, x, nn) -> None:
    """6XNN Store number NN in register VX"""
    self.v[x] = nn


def opcode_7xnn(self, x, nn) -> None:
    """7XNN Add the value NN to register VX"""
    self.v[x] = (self.v[x] + nn) & 0xff


def opcode_8xy0(self, x, y) -> None:
    """8XY0 Store the value of register VY in register VX"""
    self.v[x] = self.v[y]


def opcode_8xy1(self, x, y) -> None:
    """8XY1 Set VX to VX OR VY"""
    self.v[x] = self.v[x] | self.v[y]


def opcode_8xy2(self, x, y) -> None:
    """8XY2 Set VX to VX AND VY"""
    self.v[x] = self.v[x] & self.v[y]


def opcode_8xy3(self, x, y) -> None:
    """8XY3 Set VX to VX XOR VY"""
    self.v[x] = self.v[x] ^ self.v[y]


def opcode_8xy4(self, x, y) -> None:
    """
    8XY4 Add the value of register VY to register VX.
    Set VF to 01 if a carry occurs
    Set VF to 00 if a carry does not occur
    """

    # TODO: refactor this
    added = self.v[x] + self.v[y]
    self.v[x] = added & 0xff
    self.v[0xf] = added >> 8


def opcode_8xy5(self, x, y) -> None:
    """
    8XY5 Subtract the value of register VY from register VX
    Set VF to 00 if a borrow occurs
    Set VF to 01 if a borrow does not occur
    """

    # TODO: refactor this
    self.v[0xf] = 0x01 if self.v[x] > self.v[y] else 0x00

    subtracted = self.v[x] - self.v[y]
    self.v[x] = (0xff + subtracted) if subtracted < 0x00 else subtracted


def opcode_8xy6(self, x, y) -> None:
    """
    8XY6 Store the value of register VY shifted right one bit in register VX
    Set register VF to the least significant bit prior to the shift
    """
    self.v[0xf] = self.v[y] & 0x01
    self.v[x] = self.v[y] >> 1


def opcode_8xy7(self, x, y) -> None:
    """
    8XY7 Set register VX to the value of VY minus VX
    Set VF to 00 if a borrow occurs
    Set VF to 01 if a borrow does not occur
    """

    # TODO: refactor this
    self.v[0xf] = 0x01 if self.v[y] > self.v[x] else 0x00

    subtracted = self.v[y] - self.v[x]
    self.v[x] = (0xff + subtracted) if subtracted < 0x00 else subtracted


def opcode_8xye(self, x, y) -> None:
    """
    8XYE Store the value of register VY shifted left one bit in register VX
    Set register VF to the most significant bit prior to the shift
    """
    self.v[0xf] = (self.v[y] & 0x80) >> 7
    self.v[x] = (self.v[y] << 1) & 0xff


def opcode_9xy0(self, x, y) -> int:
    """9XY0 Skip the following instruction if the value of register VX is not equal to the value of register VY"""
    return self.pc + (4 if self.v[x] != self.v[y] else 2)


def opcode_annn(self, nnn) -> None:
    """ANNN Store memory address NNN in register I"""
    self.i = nnn


def opcode_bnnn(self, nnn) -> int:
    """BNNN Jump to address NNN + V0"""
    pc = nnn + self.v[0x0]
    # TODO: this needs to be handled by Memory, but to pass test it will be here for now
    if pc > 4096:
        raise MemoryError   # TODO: and yes, needs better error
    return pc


def opcode_cxnn(self, x, nn) -> None:
    """CXNN Set VX to a random number with a mask of NN"""
    self.v[x] = random.randint(0, 255) & nn     # TODO: assume normal RPRNG instead of actual by orignal hardware


def opcode_dxyn(self, x, y, n) -> None:
    """
    DXYN Draw a sprite at position VX, VY with N bytes of sprite data starting at the address stored in I
    Set VF to 01 if any set pixels are changed to unset, and 00 otherwise
    """
    # vx: 0-63 width col, vy: 0-31 height row

    # TODO: could use some refactoring
    def get_bits(byte_):
        for i in reversed(range(8)):
            yield (byte_ & (2 ** i)) >> i

    self.v[0xF] = 0x00
    for row, add_i in enumerate(range(n), start=self.v[y]):
        for col, bit in enumerate(get_bits(self.memory[self.i + add_i]), start=self.v[x]):
            pixel = self.screen.get(col, row)

            if pixel == 0:
                #if bit == 0:
                    # 0 xor 0 = 0 -> no need to change pixel
                    #pass
                if bit == 1:
                    # 0 xor 1 = 1 -> set pixel
                    self.screen.set(col, row)
            else:
                #if bit == 0:
                    # 1 xor 0 = 1 -> no need to change pixel
                    #pass
                if bit == 1:
                    # 1 xor 1 = 0 -> unset pixel
                    self.screen.unset(col, row)
                    self.v[0xF] = 0x01


def opcode_ex9e(self, x) -> int:
    """
    EX9E Skip the following instruction if the key corresponding to the hex value currently stored in register VX is
    pressed
    """
    return self.pc + (4 if self.keypad.is_this_key_pressed(x) else 2)


def opcode_exa1(self, x) -> int:
    """
    EXA1 Skip the following instruction if the key corresponding to the hex value currently stored in register VX is
    not pressed
    """
    return self.pc + (2 if self.keypad.is_this_key_pressed(x) else 4)


def opcode_fx07(self, x) -> None:
    """FX07 Store the current value of the delay timer in register VX"""
    self.v[x] = self.delay_timer_register


def opcode_fx0a(self, x) -> None:
    """FX0A Wait for a keypress and store the result in register VX"""
    self.v[x] = self.keypad.wait_for_keypress1(x)     # TODO: to work with guit, may need workaround (instead of return, fill v[x] outside)


def opcode_fx15(self, x) -> None:
    """FX15 Set the delay timer to the value of register VX"""
    self.delay_timer_register = self.v[x]


def opcode_fx18(self, x) -> None:
    """FX18 Set the sound timer to the value of register VX"""
    self.sound_timer_register = self.v[x]


# TODO: check possible undocumented feature in this opcode
def opcode_fx1e(self, x) -> None:
    """FX1E Add the value stored in register VX to register I"""
    self.i += self.v[x]


def opcode_fx29(self, x) -> None:
    """
    FX29 Set I to the memory address of the sprite data corresponding to the hexadecimal digit stored in register VX
    """
    self.i = self.v[x] * 5


def opcode_fx33(self, x) -> None:
    """FX33 Store the binary-coded decimal equivalent of the value stored in register VX at addresses I, I+1, and I+2"""

    # TODO: refactor this
    def get_digits(n):
        for i in (100, 10, 1):
            m = math.trunc(n / i)
            yield m
            n -= m * i

    for offset, digit in enumerate(get_digits(self.v[x]), start=self.i):
        self.memory[offset] = digit


def opcode_fx55(self, x) -> None:
    """
    FX55 Store the values of registers V0 to VX inclusive in memory starting at address I
    I is set to I + X + 1 after operation
    """
    for i in range(x + 1):
        self.memory[self.i] = self.v[i]
        self.i += 1


def opcode_fx65(self, x) -> None:
    """
    FX65 Fill registers V0 to VX inclusive with the values stored in memory starting at address I
    I is set to I + X + 1 after operation
    """

    for n in range(x + 1):
        self.v[n] = self.memory[self.i]
        self.i += 1
