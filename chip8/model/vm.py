# TODO: add docstrings

import logging

# TODO: relative imports
from chip8.model.keypad import KeyPad
from chip8.model.memory import Memory
import chip8.model.opcodes as opcodes
from chip8.model.screen import Screen

PROGRAM_START = 0x200

logging.basicConfig(level=logging.DEBUG)


# TODO: consider replacing all ints with Byte class (allows +, >, __repr__ with hex)
class VirtualMachine:

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
        # TODO: stack
        # TODO: load font set

        if program_start is not None:
            self.load_program(program_fpath)

    def load_program(self, fpath: str) -> None:
        logging.debug(f"model.vm:load_program({fpath})")

        # TODO: might still improve this
        with open(fpath, "rb") as f:
            self.memory.load_data(self.program_start, *f.read())

    def step(self) -> None:
        # fetch
        opcode = self.memory.get_opcode(self.pc)     # big-endian

        # parse
        func = self._parse_opcode(opcode)

        # execute
        args = list(self._add_args(func, opcode))
        next_pc = func(*args)
        logging.debug(f"model.vm:{hex(self.pc)}:{hex(opcode)}:{self._get_mnemonic(func, args)}")

        if self.pc == next_pc:
            raise ValueError    # TODO: raise SimpleInfiniteLoop

        self.pc = (self.pc + 2) if next_pc is None else next_pc     # TODO: 2 if the usual increment -- put in const?

    def _add_args(self, func, opcode):
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

    # TODO: need option to turn off debug
    def _get_mnemonic(self, func, args) -> str:
        # TODO: experimental code, find something better...
        # TODO: args -- convert to hex already...
        ops = {
            # TODO: better opcodes -- check cowgod?
            # opcodes.opcode_0nnn: lambda _, nnn: None,
            opcodes.opcode_00e0: lambda _: "cls",
            opcodes.opcode_00ee: lambda _: "return",
            opcodes.opcode_1nnn: lambda _, nnn: f"jump {hex(nnn)}",
            opcodes.opcode_2nnn: lambda _, nnn: f"call {hex(nnn)}",
            opcodes.opcode_3nnn: lambda _, x, nn: f"skip next if V{hex(x)[-1]} == {hex(nn)}",
            opcodes.opcode_4nnn: lambda _, x, nn: f"skip next if V{hex(x)[-1]} != {hex(nn)}",
            opcodes.opcode_5xy0: lambda _, x, y: f"skip next if V{hex(x)[-1]} == V{hex(y)[-1]}",
            opcodes.opcode_6xnn: lambda _, x, nn: f"V{hex(x)[-1]} = {hex(nn)}",
            opcodes.opcode_7xnn: lambda _, x, nn: f"V{hex(x)[-1]} += {hex(nn)}",
            opcodes.opcode_8xy0: lambda _, x, y: f"V{hex(x)[-1]} = V{hex(y)[-1]}",
            opcodes.opcode_8xy1: lambda _, x, y: f"V{hex(x)[-1]} = V{hex(y)[-1]} or V{hex(y)[-1]}",
            opcodes.opcode_8xy2: lambda _, x, y: f"V{hex(x)[-1]} = V{hex(y)[-1]} and V{hex(y)[-1]}",
            opcodes.opcode_8xy3: lambda _, x, y: f"V{hex(x)[-1]} = V{hex(y)[-1]} xor V{hex(y)[-1]}",
            opcodes.opcode_8xy4: lambda _, x, y: f"V{hex(x)[-1]} += V{hex(y)[-1]}; VF = carry",
            opcodes.opcode_8xy5: lambda _, x, y: f"V{hex(x)[-1]} -= V{hex(y)[-1]}; VF = borrow",
            opcodes.opcode_8xy6: lambda _, x, y: f"V{hex(x)[-1]} = V{hex(y)[-1]} >> 1; VF = lsb",
            opcodes.opcode_8xy7: lambda _, x, y: f"V{hex(x)[-1]} = V{hex(y)[-1]} - V{hex(x)[-1]}; VF = borrow",
            opcodes.opcode_8xye: lambda _, x, y: f"V{hex(x)[-1]} = V{hex(y)[-1]} << 1; VF = msb",
            opcodes.opcode_9xy0: lambda _, x, y: f"skip next if V{hex(x)[-1]} != V{hex(y)[-1]}",
            opcodes.opcode_annn: lambda _, nnn: f"I = {hex(nnn)}",
            opcodes.opcode_bnnn: lambda _, nnn: f"jump {hex(nnn)} + V0 (jump {hex(nnn + self.v[0])})",
            opcodes.opcode_cxnn: lambda _, x, nn: f"V{hex(x)[-1]} = rnd() with mask {hex(nn)}",
            opcodes.opcode_dxyn: lambda _, x, y, n: f"draw {hex(n)} bytes of sprite data to V{hex(x)[-1]}, V{hex(y)[-1]}",
            opcodes.opcode_ex9e: lambda _, x: f"skip next if keypress() == V{hex(x)[-1]}",
            opcodes.opcode_exa1: lambda _, x: f"skip next if keypress() != V{hex(x)[-1]}",
            opcodes.opcode_fx07: lambda _, x: f"V{hex(x)[-1]} = delay_timer",   # (V{hex(x)[-1]} = {hex(self.delay_timer)}",
            opcodes.opcode_fx0a: lambda _, x: f"V{hex(x)[-1]} = input()",
            opcodes.opcode_fx15: lambda _, x: f"delay_timer = V{hex(x)[-1]}",
            opcodes.opcode_fx18: lambda _, x: f"sound_timer = V{hex(x)[-1]}",
            opcodes.opcode_fx1e: lambda _, x: f"I += V{hex(x)[-1]}",
            opcodes.opcode_fx29: lambda _, x: f"I = sprite_data(V{hex(x)[-1]})",
            opcodes.opcode_fx33: lambda _, x: f"memory[I:] = BCD(V{hex(x)[-1]})",
            opcodes.opcode_fx55: lambda _, x: f"memory[I:] = V[0:hex(x)[-1]nclusive]; I = I + hex(x) + 1",
            opcodes.opcode_fx65: lambda _, x: f"V[0:hex(x)[-1]nclusive] = memory[I:]; I = I + hex(x) + 1",
        }
        return ops[func](*args)     # TODO: two *, check performance

    def _parse_opcode(self, opcode: int):   # -> function:
        # TODO: improve this
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
