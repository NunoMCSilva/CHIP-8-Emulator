import pytest

from chip8.vm import VirtualMachine


# TODO: put in TestVM?
@pytest.fixture
def vm():
    return VirtualMachine()


class TestVirtualMachineStep:

    # Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior]
    def test_opcode_0nnn__raises_not_implemented_error(self, vm):
        # 0NNN Execute machine language subroutine at address NNN

        # arrange
        vm.memory.load_opcodes(0x200, 0x0123)

        # act & assert
        with pytest.raises(NotImplementedError):    # TODO: better exception?
            vm.step()
        # TODO: check message? -- "this instruction is highly considered deprecated, as it often remains unimplemented on modern interpreters"

    def test_opcode_00e0__clears_screen(self, mocker, vm):
        # 00E0 Clear the screen

        # arrange
        vm.memory.load_opcodes(0x200, 0x00E0)

        mocker.spy(vm.screen, "clear")

        # act
        vm.step()

        # assert
        assert vm.screen.clear.call_count == 1
        assert vm.pc == 0x202

    # TODO: need to test behaviour if stack == [] -- not found in documentation yet
    def test_opcode_00ee__returns_from_subroutine(self, vm):
        # 00EE Return from a subroutine

        # arrange
        vm.memory.load_opcodes(0x200, 0x00EE)
        vm.stack = [0xFFF, 0x300]

        # act
        vm.step()

        # assert
        assert vm.stack == [0xFFF]
        assert vm.pc == 0x300

    def test_opcode_1nnn__jumps_to_address_nnn(self, vm):
        # 1NNN Jump to address NNN

        # arrange
        vm.memory.load_opcodes(0x200, 0x1abc)     # TODO: vm.load_program, not vm.memory.load_bytes

        # act
        vm.step()

        # assert
        assert vm.pc == 0xabc

    # TODO: need to test when stack is greater than 16x -- check what happens
    def test_opcode_2nnn__calls_subroutine_starting_at_address_nnn(self, vm):
        # 2NNN Execute subroutine starting at address NNN

        # arrange
        vm.memory.load_opcodes(0x200, 0x2345)

        # act
        vm.step()

        # assert
        assert vm.pc == 0x345
        assert vm.stack == [0x200]

    def test_opcode_3xnn_with_vx_equal_to_nn__skip_next_instruction(self, vm):
        # 3XNN Skip the following instruction if the value of register VX equals NN

        # arrange
        vm.memory.load_opcodes(0x200, 0x3a11)
        vm.v[0xA] = 0x11

        # act
        vm.step()

        # assert
        assert vm.pc == 0x204

    def test_opcode_3xnn_with_vx_not_equal_to_nn__do_not_skip_next_instruction(self, vm):
        # 3XNN Skip the following instruction if the value of register VX equals NN

        # arrange
        vm.memory.load_opcodes(0x200, 0x3a11)
        vm.v[0xA] = 0x34

        # act
        vm.step()

        # assert
        assert vm.pc == 0x202

    def test_opcode_4xnn_with_vx_not_equal_to_nn__skip_next_instruction(self, vm):
        # 4XNN Skip the following instruction if the value of register VX is not equal to NN

        # arrange
        vm.memory.load_opcodes(0x200, 0x4233)
        vm.v[0x2] = 0x35

        # act
        vm.step()

        # assert
        assert vm.pc == 0x204

    def test_opcode_4xnn_with_vx_equal_to_nn__do_not_skip_next_instruction(self, vm):
        # 4XNN Skip the following instruction if the value of register VX is not equal to NN

        # arrange
        vm.memory.load_opcodes(0x200, 0x4233)
        vm.v[0x2] = 0x33

        # act
        vm.step()

        # assert
        assert vm.pc == 0x202

    def test_opcode_5xy0_with_vx_equal_to_vy__skip_next_instruction(self, vm):
        # 5XY0 Skip the following instruction if the value of register VX is equal to the value of register VY

        # arrange
        vm.memory.load_opcodes(0x200, 0x5630)
        vm.v[0x6] = vm.v[0x3] = 0x14

        # act
        vm.step()

        # assert
        assert vm.pc == 0x204

    def test_opcode_5xy0_with_vx_not_equal_to_vy__do_not_skip_next_instruction(self, vm):
        # 5XY0 Skip the following instruction if the value of register VX is equal to the value of register VY

        # arrange
        vm.memory.load_opcodes(0x200, 0x5630)
        vm.v[0x6] = 0x12
        vm.v[0x3] = 0x14

        # act
        vm.step()

        # assert
        assert vm.pc == 0x202

    def test_opcode_6xnn__nn_is_stored_in_vx(self, vm):
        # 6XNN Store number NN in register VX

        # arrange
        vm.memory.load_opcodes(0x200, 0x6abc)

        # act
        vm.step()

        # assert
        assert vm.v[0xa] == 0xbc
        assert vm.pc == 0x202

    # TODO: parametrize above/below?
    def test_opcode_7xnn__nn_is_added_to_vx_with_added_value_being_below_255(self, vm):
        # 7XNN Add the value NN to register VX

        # arrange
        vm.memory.load_opcodes(0x200, 0x7e25)
        vm.v[0xe] = 0x05

        # act
        vm.step()

        # assert
        assert vm.v[0xe] == 0x2A
        assert vm.pc == 0x202

    def test_opcode_7xnn__nn_is_added_to_vx_with_added_value_above_255(self, vm):
        # 7XNN Add the value NN to register VX

        # arrange
        vm.memory.load_opcodes(0x200, 0x7eff)
        vm.v[0xe] = 0xff

        # act
        vm.step()

        # assert
        assert vm.v[0xe] == 0xfe
        assert vm.pc == 0x202

    def test_opcode_8xy0__vy_is_stored_in_vx(self, vm):
        # 8XY0 Store the value of register VY in register VX

        # arrange
        vm.memory.load_opcodes(0x200, 0x8120)
        vm.v[0x2] = 0xEE

        # act
        vm.step()

        # assert
        assert vm.v[0x1] == 0xEE
        assert vm.pc == 0x202

    def test_opcode_8xy1__vx_bitwise_or_vy_is_stored_in_vx(self, vm):
        # 8XY1 	Set VX to VX OR VY

        # arrange
        vm.memory.load_opcodes(0x200, 0x8341)
        vm.v[0x3] = 0x28
        vm.v[0x4] = 0xA3

        # act
        vm.step()

        # assert
        assert vm.v[0x3] == 0xAB
        assert vm.pc == 0x202

    def test_opcode_8xy2__vx_bitwise_and_vy_is_stored_in_vx(self, vm):
        # 8XY2 	Set VX to VX AND VY

        # arrange
        vm.memory.load_opcodes(0x200, 0x8562)
        vm.v[0x5] = 0x2B
        vm.v[0x6] = 0xA3

        # act
        vm.step()

        # assert
        assert vm.v[0x5] == 0x23
        assert vm.pc == 0x202

    # TODO: add cases for xy being xx?
    def test_opcode_8xy3__bitwise_vx_xor_vy_is_stored_in_vx(self, vm):
        # 8XY3 	Set VX to VX XOR VY

        # arrange
        vm.memory.load_opcodes(0x200, 0x8aB3)
        vm.v[0xA] = 0x2B
        vm.v[0xB] = 0xA3

        # act
        vm.step()

        # assert
        assert vm.v[0xA] == 0x88
        assert vm.pc == 0x202

    # TODO: parametrize carry?
    def test_opcode_8xy4__vy_is_added_to_vx_without_carry(self, vm):
        # 8XY4 	Add the value of register VY to register VX
        # Set VF to 01 if a carry occurs
        # Set VF to 00 if a carry does not occur

        # arrange
        vm.memory.load_opcodes(0x200, 0x8284)
        vm.v[0x2] = 0x10
        vm.v[0x8] = 0x20

        # act
        vm.step()

        # assert
        assert vm.v[0x2] == 0x30
        assert vm.v[0xf] == 0x00    # no carry
        assert vm.pc == 0x202

    def test_opcode_8xy4__vy_is_added_to_vx_with_carry(self, vm):
        # 8XY4 	Add the value of register VY to register VX
        # Set VF to 01 if a carry occurs
        # Set VF to 00 if a carry does not occur

        # arrange
        vm.memory.load_opcodes(0x200, 0x8284)
        vm.v[0x2] = 0xff
        vm.v[0x8] = 0x20

        # act
        vm.step()

        # assert
        assert vm.v[0x2] == 0x1f
        assert vm.v[0xf] == 0x01    # carry
        assert vm.pc == 0x202

    # TODO: this and 8xy7 are trick, recheck docs well
    # TODO: parametrize borrow?
    def test_opcode_8xy5__vx_minus_vy_is_stored_in_vx_without_borrow(self, vm):
        # 8XY5 	Subtract the value of register VY from register VX
        # Set VF to 00 if a borrow occurs
        # Set VF to 01 if a borrow does not occur

        # arrange
        vm.memory.load_opcodes(0x200, 0x8285)
        vm.v[0x2] = 0x0B    # Vx
        vm.v[0x8] = 0x05    # Vy

        # act
        vm.step()

        # assert
        assert vm.v[0x2] == 0x06    # Vy = Vx - Vy
        assert vm.v[0xF] == 0x01    # no borrow
        assert vm.pc == 0x202

    # TODO: this and 8xy7 are trick, recheck docs well
    def test_opcode_8yx5__vx_minus_vy_is_stored_in_vx_with_borrow(self, vm):
        # 8XY5 	Subtract the value of register VY from register VX
        # Set VF to 00 if a borrow occurs
        # Set VF to 01 if a borrow does not occur

        # arrange
        vm.memory.load_opcodes(0x200, 0x8285)
        vm.v[0x2] = 0x0B    # Vx
        vm.v[0x8] = 0x0C    # Vy

        # act
        vm.step()

        # assert
        assert vm.v[0x2] == 0xFE    # Vy = Vx - Vy
        assert vm.v[0xF] == 0x00    # borrow
        assert vm.pc == 0x202

    @pytest.mark.parametrize('vy, vf', [(0x1f, 0x01), (0x1e, 0x00)])
    def test_opcode_8xy6__vy_shifted_right_by_one_bit_stored_in_vx_and_lsb_of_vy_stored_in_vf(self, vm, vy, vf):
        # 8XY6 	Store the value of register VY shifted right one bit in register VX
        # Set register VF to the least significant bit prior to the shift

        # arrange
        vm.memory.load_opcodes(0x200, 0x8AB6)
        vm.v[0xB] = vy

        # act
        vm.step()

        # assert
        assert vm.v[0xA] == 0x0f
        assert vm.v[0xB] == vy
        assert vm.v[0xF] == vf
        assert vm.pc == 0x202

    # TODO: this and 8xy5 are trick, recheck docs well
    # TODO: parametrize borrow?
    def test_opcode_8xy7__vy_minus_vx_is_stored_in_vx_without_borrow(self, vm):
        # 8XY7 	Set register VX to the value of VY minus VX
        # Set VF to 00 if a borrow occurs
        # Set VF to 01 if a borrow does not occur

        # arrange
        vm.memory.load_opcodes(0x200, 0x8287)
        vm.v[0x2] = 0x11    # Vx
        vm.v[0x8] = 0x20    # Vy

        # step
        vm.step()

        # assert
        assert vm.v[0x2] == 0x0f    # Vy = Vy - Vx
        assert vm.v[0xf] == 0x01    # no borrow
        assert vm.pc == 0x202

    # TODO: this and 8xy5 are trick, recheck docs well
    def test_opcode_8xy7__vy_minus_vx_is_stored_in_vx_with_borrow(self,vm):
        # 8XY7 	Set register VX to the value of VY minus VX
        # Set VF to 00 if a borrow occurs
        # Set VF to 01 if a borrow does not occur

        # arrange
        vm.memory.load_opcodes(0x200, 0x8287)
        vm.v[0x2] = 0x22    # vx
        vm.v[0x8] = 0x20    # vy

        # step
        vm.step()

        # assert
        assert vm.v[0x2] == 0xfd    # Vy = Vy - Vx
        assert vm.v[0xf] == 0x00    # borrow
        assert vm.pc == 0x202

    @pytest.mark.parametrize('vy, vf', [(0xff, 0x01), (0x7f, 0x00)])
    def test_opcode_8xye__vy_shifted_left_by_one_bit_stored_in_vx_and_msb_of_vy_stored_in_vf(self, vm, vy, vf):
        # 8XYE 	Store the value of register VY shifted left one bit in register VX
        # Set register VF to the most significant bit prior to the shift

        # arrange
        vm.memory.load_opcodes(0x200, 0x8cbe)
        vm.v[0xb] = vy

        # act
        vm.step()

        # assert
        assert vm.v[0xc] == 0xfe
        assert vm.v[0xf] == vf
        assert vm.pc == 0x202

    def test_opcode_9xy0_with_vx_not_equal_to_vy__skip_next_instruction(self, vm):
        # 9XY0 	Skip the following instruction if the value of register VX is not equal to the value of register VY

        # arrange
        vm.memory.load_opcodes(0x200, 0x9630)
        vm.v[0x6] = 0x12
        vm.v[0x3] = 0x14

        # act
        vm.step()

        # assert
        assert vm.pc == 0x204

    # TODO: hmm, some of these conditional branching tests can be collapsed into a "parametrized" super test...
    def test_opcode_9xy0_with_vx_equal_to_vy__do_not_skip_next_instruction(self, vm):
        # 9XY0 	Skip the following instruction if the value of register VX is not equal to the value of register VY

        # arrange
        vm.memory.load_opcodes(0x200, 0x9630)         # TODO: vm.memory.load_opcodes() vs vm.memory.load_data
        vm.v[0x6] = vm.v[0x3] = 0x14

        # act
        vm.step()

        # assert
        assert vm.pc == 0x202

    def test_opcode_annn__nnn_stored_in_register_i(self, vm):
        # ANNN 	Store memory address NNN in register I

        # arrange
        vm.memory.load_opcodes(0x200, 0xa123)

        # act
        vm.step()

        # assert
        assert vm.i == 0x123
        assert vm.pc == 0x202   # TODO: check if it's possible to add a post_test test to this to simplify code...

    # TODO: add vm as pre-test to all these? (setup) instead of fixture?
    def test_opcode_bnnn__jumps_to_address_nnn_plus_v0(self, vm):
        # BNNN 	Jump to address NNN + V0

        # arrange
        vm.memory.load_opcodes(0x200, 0xb345)     # TODO: put 0x200 in CONST
        vm.v[0x0] = 0xFF

        # act
        vm.step()

        # assert
        assert vm.pc == 0x345 + 0xff

    def test_opcode_bnnn_with_nnn_plus_v0_equal_outside_memory__raise_memory_error(self, vm):
        # BNNN 	Jump to address NNN + V0

        # arrange
        vm.memory.load_opcodes(0x200, 0xbFFF)
        vm.v[0x0] = 0xFF
        # 0xFFF + 0xFF = 0x10FE, which is out of memory on a 4KiB system
        # TODO: improve this comment

        # act & assert
        with pytest.raises(MemoryError):    # TODO: need much better exception -- create one
            vm.step()

    def test_opcode_cxnn__sets_vx_to_random_number_with_mask_of_nn(self, mocker, vm):
        # CXNN 	Set VX to a random number with a mask of NN

        # arrange
        vm.memory.load_opcodes(0x200, 0xC864)

        mocker.patch("random.randint").return_value = 0x25

        # act
        vm.step()

        # assert
        assert vm.v[0x8] == 0x24    # 0x24 AND 0x64
        assert vm.pc == 0x202

    def test_opcode_dxyn_with_empty_screen__puts_0_in_screen_and_put_not_collision_in_vf(self, mocker, vm):
        # DXYN 	Draw a sprite at position VX, VY with N bytes of sprite data starting at the address stored in I
        # Set VF to 01 if any set pixels are changed to unset, and 00 otherwise

        # arrange
        vm.memory.load_opcodes(0x200, 0xDAB5)
        vm.v[0xa] = 0x00
        vm.v[0xb] = 0x00

        mocker.spy(vm.screen, "set")

        # TODO: check order of set screen according to spec
        expected_call_args_list = [mocker.call(*t) for t in (
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (3, 1),
            (0, 2), (3, 2),
            (0, 3), (3, 3),
            (0, 4), (1, 4), (2, 4), (3, 4),
        )]

        # act
        vm.step()

        # assert
        assert vm.screen.set.call_args_list == expected_call_args_list
        assert vm.i == 0x0000       # no change
        assert vm.v[0xf] == 0x00    # no collision
        assert vm.pc == 0x202

    def test_opcode_dxyn_with_empty_screen__puts_wrapped_0_in_screen_and_put_not_collision_in_vf(self, mocker, vm):
        # DXYN 	Draw a sprite at position VX, VY with N bytes of sprite data starting at the address stored in I
        # Set VF to 01 if any set pixels are changed to unset, and 00 otherwise

        # arrange
        vm.memory.load_opcodes(0x200, 0xDAB5)
        vm.v[0xa] = 62
        vm.v[0xb] = 30

        mocker.spy(vm.screen, "set")

        # TODO: check order of set screen according to spec
        expected_call_args_list = [mocker.call(*t) for t in (
            (62, 30), (63, 30), (64, 30), (65, 30),
            (62, 31), (65, 31),
            (62, 32), (65, 32),
            (62, 33), (65, 33),
            (62, 34), (63, 34), (64, 34), (65, 34),
        )]

        # act
        vm.step()

        # assert
        assert vm.screen.set.call_args_list == expected_call_args_list
        assert vm.i == 0x0000       # no change
        assert vm.v[0xf] == 0x00    # no collision
        assert vm.pc == 0x202

    def test_opcode_dxyn00_with_one_pixel_on_screen__unset_pixel_and_put_collision_in_vf(self, mocker, vm):
        # DXYN Draw a sprite at position VX, VY with N bytes of sprite data starting at the address stored in I
        # Set VF to 01 if any set pixels are changed to unset, and 00 otherwise

        # arrange
        vm.memory.load_opcodes(0x200, 0xd311)
        vm.v[0x3] = 1  # x
        vm.v[0x1] = 1  # y

        vm.memory[0x0000] = 0b10000000
        vm.screen.set(1, 1)

        mocker.spy(vm.screen, "unset")

        # act
        vm.step()

        # assert
        assert vm.screen.unset.call_args_list == [mocker.call(1, 1)]
        assert vm.i == 0x0000       # no change
        assert vm.v[0xf] == 0x01    # collision
        assert vm.pc == 0x202

    def test_opcode_ex9e_with_key_pressed__skip_next_instruction(self, mocker, vm):
        # EX9E Skip the following instruction if the key corresponding to the hex value currently stored in register
        # VX is pressed

        # arrange
        vm.memory.load_opcodes(0x200, 0xE19E)
        vm.v[0x1] = 0x05

        mocker.patch.object(vm.keypad, "is_this_key_pressed").return_value = True

        # act
        vm.step()

        # assert
        assert vm.pc == 0x204

    def test_opcode_ex9e_with_key_not_pressed__do_not_skip_next_instruction(self, mocker, vm):
        # EX9E Skip the following instruction if the key corresponding to the hex value currently stored in register
        # VX is pressed

        # arrange
        vm.memory.load_opcodes(0x200, 0xE19E)
        vm.v[0x1] = 0x05
        mocker.patch.object(vm.keypad, "is_this_key_pressed").return_value = False

        # act
        vm.step()

        # assert
        assert vm.pc == 0x202

    def test_opcode_exa1_with_key_not_pressed__skip_next_instruction(self, mocker, vm):
        # EXA1 Skip the following instruction if the key corresponding to the hex value currently stored in register
        # VX is not pressed

        # arrange
        vm.memory.load_opcodes(0x200, 0xE1A1)
        vm.v[0x1] = 0x0A
        mocker.patch.object(vm.keypad, "is_this_key_pressed").return_value = False

        # act
        vm.step()

        # assert
        assert vm.pc == 0x204

    def test_opcode_exa1_with_key_pressed__do_not_skip_next_instruction(self, mocker, vm):
        # EXA1 Skip the following instruction if the key corresponding to the hex value currently stored in register
        # VX is not pressed

        # arrange
        vm.memory.load_opcodes(0x200, 0xE1A1)
        vm.v[0x1] = 0x0A
        mocker.patch.object(vm.keypad, "is_this_key_pressed").return_value = True

        # act
        vm.step()

        # assert
        assert vm.pc == 0x202

    def test_opcode_fx07__stored_delay_timer_in_vx(self, vm):
        # FX07 	Store the current value of the delay timer in register VX

        # arrange
        vm.memory.load_opcodes(0x200, 0xf507)
        vm.delay_timer_register = 0x33

        # act
        vm.step()

        # assert
        assert vm.delay_timer_register == 0x33  # TODO: does timer is dec before or after opc -- this value if before
        assert vm.v[0x5] == 0x33
        assert vm.pc == 0x202

    def test_opcode_fx0a__stored_result_of_waited_keypress_in_vx(self, mocker, vm):
        # FX0A 	Wait for a keypress and store the result in register VX

        # arrange
        vm.memory.load_opcodes(0x200, 0xF30A)
        mocker.patch.object(vm.keypad, "wait_for_keypress").return_value = 0x0B

        # act
        vm.step()

        # assert
        assert vm.v[0x3] == 0x0B
        assert vm.pc == 0x202

    def test_opcode_fx15__delay_time_changed_to_vx(self, vm):
        # FX15 	Set the delay timer to the value of register VX

        # arrange
        vm.memory.load_opcodes(0x200, 0xfa15)
        vm.v[0xa] = 0xff

        # act
        vm.step()

        # assert
        assert vm.delay_timer_register == 0xff  # TODO: does timer is dec before or after opc -- this value if before
        assert vm.v[0xa] == 0xff
        assert vm.pc == 0x202

    def test_opcode_fx18__sound_timer_changed_to_vx(self, vm):
        # FX18 	Set the sound timer to the value of register VX

        # arrange
        vm.memory.load_opcodes(0x200, 0xf918)
        vm.v[0x9] = 0x25

        # act
        vm.step()

        # assert
        assert vm.sound_timer_register == 0x25  # TODO: does timer is dec before or after opc -- this value if before
        assert vm.v[0x9] == 0x25
        assert vm.pc == 0x202

    def test_opcode_fx1e__add_vx_to_i(self, vm):
        # FX1E 	Add the value stored in register VX to register I

        # arrange
        vm.memory.load_opcodes(0x200, 0xf31e)
        vm.v[0x3] = 0x44

        # act
        vm.step()

        # assert
        assert vm.i == 0x0044
        assert vm.pc == 0x202

        # TODO: check if undocumented feature exists -- check source -- david winter?
        """
        fx1e
            # Adds VX to I. VF is set to 1 when there is a range overflow (I+VX>0xFFF), and to 0 when there isn't.
            # This is an undocumented feature of the CHIP-8 and used by the Spacefight 2091! game.
            added = self.i + self.v[x]
            self.i = added
            self.v[0xf] = 0x01 if added > 0xfff else 0x00
        """

    def test_opcode_fx29__i_set_to_memory_address_of_sprite_data_corresponding_to_hex_digit_stored_in_vx(self, vm):
        # FX29 Set I to the memory address of the sprite data corresponding to the hexadecimal digit stored in
        # register VX

        # arrange
        vm.memory.load_opcodes(0x200, 0xf429)
        vm.v[0x4] = 0x03

        # act
        vm.step()

        # assert
        assert vm.i == 0x000f
        assert vm.pc == 0x202

    def test_opcode_fx33__bcd_of_vx_stored_in_memory_starting_at_address_i(self, vm):
        # FX33 Store the binary-coded decimal equivalent of the value stored in register VX at addresses I, I+1, and I+2

        # arrange
        vm.memory.load_opcodes(0x200, 0xf233)
        vm.v[0x2] = 172
        vm.i = 0x250

        # act
        vm.step()

        # assert
        # TODO: which representation of BCD? use natural BCD?
        assert vm.memory[0x250] == 0b0001
        assert vm.memory[0x251] == 0b0111
        assert vm.memory[0x252] == 0b0010
        assert vm.pc == 0x202

    def test_opcode_fx55__register_v0_to_vx_inclusive_stored_in_memory_starting_at_address_i(self, vm):
        # FX55 Store the values of registers V0 to VX inclusive in memory starting at address I
        # I is set to I + X + 1 after operation

        # arrange
        vm.memory.load_opcodes(0x200, 0xf355)

        for i, value in enumerate([0xAA, 0xB2, 0xC9, 0xD1]):
            vm.v[i] = value

        vm.i = 0x250

        # act
        vm.step()

        # assert
        assert vm.i == 0x254    # TODO: check this well, seems to contradict other data
        assert vm.memory[0x250] == vm.v[0x0] == 0xAA
        assert vm.memory[0x251] == vm.v[0x1] == 0xB2
        assert vm.memory[0x252] == vm.v[0x2] == 0xC9
        assert vm.memory[0x253] == vm.v[0x3] == 0xD1
        assert vm.pc == 0x202

    def test_opcode_fx65__registers_v0_to_vx_inclusive_filled_with_values_stored_in_mem_starting_at_address_i(self, vm):
        # FX65 	Fill registers V0 to VX inclusive with the values stored in memory starting at address I
        # I is set to I + X + 1 after operation

        # arrange
        vm.memory.load_opcodes(0x200, 0xf465)
        vm.memory.load_data(0x250, 0x12, 0x34, 0x56, 0x78, 0xAB)
        vm.i = 0x250

        # act
        vm.step()

        # assert
        assert vm.i == 0x255
        assert vm.memory[0x250] == vm.v[0x0] == 0x12
        assert vm.memory[0x251] == vm.v[0x1] == 0x34
        assert vm.memory[0x252] == vm.v[0x2] == 0x56
        assert vm.memory[0x253] == vm.v[0x3] == 0x78
        assert vm.memory[0x254] == vm.v[0x4] == 0xAB
        assert vm.pc == 0x202
