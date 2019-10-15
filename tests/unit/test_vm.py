import pytest

from chip8.vm import Chip8VirtualMachine


@pytest.fixture
def vm():
    return Chip8VirtualMachine()


def test_opcode_00e0(mocker, vm):
    # arrange
    mocker.spy(vm.screen, "clear")

    # act
    vm._opcode_00e0()

    # assert
    assert vm.screen.clear.call_count == 1
