from chip8.screen import Chip8Screen


class Chip8VirtualMachine:

    def __init__(self):
        self.screen = Chip8Screen()

    def _opcode_00e0(self) -> None:
        """Clear the screen"""
        # TODO: verify if behaviour is correct according to "Mastering the CHIP-8"
        self.screen.clear()
        self.pc += 2    # TODO: untested part -- later

    def _opcode_00ee(self) -> None:
        """Return from a subroutine"""
        # TODO: verify if behaviour is correct according to "Mastering the CHIP-8"
        # TODO: check behaviour on return when stack is empty
        pass

    def _opcode_0nnn(self, nnn: int) -> None:
        """Execute machine language subroutine at address NNN"""
        pass

    def _opcode_1nnn(self, nnn: int) -> None:
        """Jump to address NNN"""
        pass

    def _opcode_(self) -> None:
        """2NNN 	Execute subroutine starting at address NNN"""
        pass

    def _opcode_(self) -> None:
        """3XNN 	Skip the following instruction if the value of register VX equals NN"""
        pass

    def _opcode_(self) -> None:
        """4XNN 	Skip the following instruction if the value of register VX is not equal to NN"""
        pass

    def _opcode_(self) -> None:
        """5XY0 	Skip the following instruction if the value of register VX is equal to the value of register VY"""
        pass

    def _opcode_(self) -> None:
        """6XNN 	Store number NN in register VX"""
        pass

    def _opcode_(self) -> None:
        """7XNN 	Add the value NN to register VX"""
        pass

    def _opcode_(self) -> None:
        """8XY0 	Store the value of register VY in register VX"""
        pass

    def _opcode_(self) -> None:
        """8XY1 	Set VX to VX OR VY"""
        pass

    def _opcode_(self) -> None:
        """8XY2 	Set VX to VX AND VY"""
        pass

    def _opcode_(self) -> None:
        """8XY3 	Set VX to VX XOR VY"""
        pass

    def _opcode_(self) -> None:
        """8XY4 	Add the value of register VY to register VX
Set VF to 01 if a carry occurs
Set VF to 00 if a carry does not occur"""
        pass

    def _opcode_(self) -> None:
        """8XY5 	Subtract the value of register VY from register VX
Set VF to 00 if a borrow occurs
Set VF to 01 if a borrow does not occur
"""
        pass

    def _opcode_(self) -> None:
        """8XY6 	Store the value of register VY shifted right one bit in register VX
Set register VF to the least significant bit prior to the shift
"""
        pass

    def _opcode_(self) -> None:
        """8XY7 	Set register VX to the value of VY minus VX
Set VF to 00 if a borrow occurs
Set VF to 01 if a borrow does not occur
"""
        pass

    def _opcode(self) -> None:
        """"""
        pass

    def _opcode(self) -> None:
        """"""
        pass

    def _opcode(self) -> None:
        """"""
        pass





"""





8XYE 	Store the value of register VY shifted left one bit in register VX
Set register VF to the most significant bit prior to the shift
9XY0 	Skip the following instruction if the value of register VX is not equal to the value of register VY
ANNN 	Store memory address NNN in register I
BNNN 	Jump to address NNN + V0
CXNN 	Set VX to a random number with a mask of NN
DXYN 	Draw a sprite at position VX, VY with N bytes of sprite data starting at the address stored in I
Set VF to 01 if any set pixels are changed to unset, and 00 otherwise
EX9E 	Skip the following instruction if the key corresponding to the hex value currently stored in register VX is pressed
EXA1 	Skip the following instruction if the key corresponding to the hex value currently stored in register VX is not pressed
FX07 	Store the current value of the delay timer in register VX
FX0A 	Wait for a keypress and store the result in register VX
FX15 	Set the delay timer to the value of register VX
FX18 	Set the sound timer to the value of register VX
FX1E 	Add the value stored in register VX to register I
FX29 	Set I to the memory address of the sprite data corresponding to the hexadecimal digit stored in register VX
FX33 	Store the binary-coded decimal equivalent of the value stored in register VX at addresses I, I+1, and I+2
FX55 	Store the values of registers V0 to VX inclusive in memory starting at address I
I is set to I + X + 1 after operation
FX65 	Fill registers V0 to VX inclusive with the values stored in memory starting at address I
I is set to I + X + 1 after operation
"""