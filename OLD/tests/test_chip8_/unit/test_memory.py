# TODO: improve function names

import pytest

from chip8_.memory import Memory


@pytest.fixture
def memory():
    return Memory()


def test_init__x__x(memory):
    assert len(memory) == 4 * 1024
    assert set(memory) == {0x00}


def test_get_opcode__x__x(memory):
    # arrange
    memory[0x200] = 0x12
    memory[0x201] = 0x34

    # act
    opcode = memory.get_opcode(0x200)

    # assert
    assert opcode == 0x1234


def test_load_data__x__x(memory):
    # arrange
    data = 0x23, 0x45, 0x99

    # act
    memory.load_data(0x200, *data)

    # assert
    assert tuple(memory[0x200:0x203]) == data


def test_load_opcodes__x__x(memory):
    # arrange
    opcodes = 0x1234, 0x3456, 0xFF99
    expected_data = 0x12, 0x34, 0x34, 0x56, 0xFF, 0x99

    # act
    memory.load_opcodes(0x300, *opcodes)

    # assert
    assert tuple(memory[0x300:0x306]) == expected_data


@pytest.mark.skip
def test_save__x__x(memory):
    pass


@pytest.mark.skip
def test_load__x__x(memory):
    pass
