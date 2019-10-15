"""
import pytest

from chip8.vm import Chip8VirtualMachine
import chip8.opcodes as opcodes


@pytest.fixture
def vm():
    return Chip8VirtualMachine()


def test_opcode_00e0(vm, mocker):
    # arrange
    mocker.spy(vm.screen, "clear_screen")

    # act
    opcodes.opcode_00e0(vm)

    # assert
    assert vm.screen.cls.call_count == 1

"""
"""
def test_00e0(mocker):
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x00
    vm.memory[0x201] = 0xe0

    mocker.spy(vm.screen, "cls")

    # act
    vm.step()
    # will work by xor

    # assert
    assert vm.screen.cls.call_count == 1
    assert vm.pc == 0x202




def test_opcode_0nnn(vm):
    # arrange
    vm.loadl(0x200, 0x0123)

    # act & assert
    with pytest.raises(NotImplementedError):
        vm.step()
"""
