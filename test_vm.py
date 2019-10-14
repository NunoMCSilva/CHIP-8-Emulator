# TODO: refactor

import pytest

from vm import Chip8VirtualMachine


@pytest.fixture
def vm():
    return Chip8VirtualMachine()


class TestChip8VirtualMachine:

    # Assign opcode
    def test_8xy0(self, vm):
        # arrange
        vm.loadl(0x200, 0x8120)
        vm.v[0x1] = 0xFF
        vm.v[0x2] = 0xEE

        # act
        vm.step()

        # arrange
        assert vm.v[0x1] == 0xEE
        assert vm.pc == 0x202

    # BCD opcode
    def test_fx33(self, vm):
        # arrange
        vm.loadl(0x200, 0xf233)
        vm.v[0x2] = 0xac    # 0xac == 172
        vm.i = 0x250

        # act
        vm.step()

        # assert
        # TODO: which representation of BCD? use natural BCD?
        assert vm.memory[0x250] == 0b0001
        assert vm.memory[0x251] == 0b0111
        assert vm.memory[0x252] == 0b0010
        assert vm.pc == 0x202

    # BitOp opcodes
    def test_8xy1(self, vm):
        # arrange
        vm.loadl(0x200, 0x8341)
        vm.v[0x3] = 0x2B
        vm.v[0x4] = 0xA3

        # act
        vm.step()

        # assert
        assert vm.v[0x3] == 0xAB
        assert vm.pc == 0x202

    def test_8xy2(self, vm):
        # arrange
        vm.loadl(0x200, 0x8562)
        vm.v[0x5] = 0x2B
        vm.v[0x6] = 0xA3

        # act
        vm.step()

        # assert
        assert vm.v[0x5] == 0x23
        assert vm.pc == 0x202

    # TODO: add cases for xy being xx
    def test_8xy3(self, vm):
        # arrange
        vm.loadl(0x200, 0x8aB3)
        vm.v[0xA] = 0x2B
        vm.v[0xB] = 0xA3

        # act
        vm.step()

        # assert
        assert vm.v[0xA] == 0x88
        assert vm.pc == 0x202

    @pytest.mark.parametrize('va, vf', [(0x1f, 0x01), (0x1e, 0x00)])
    def test_8xy6(self, vm, va, vf):
        # TODO: what is the use of y?
        # arrange
        vm.loadl(0x200, 0x8ab6)
        vm.v[0xa] = va

        # act
        vm.step()

        # assert
        assert vm.v[0xa] == 0x0f
        assert vm.v[0xf] == vf
        assert vm.pc == 0x202

    @pytest.mark.parametrize('vb, vf', [(0xff, 0x01), (0x7f, 0x00)])
    def test_8xye(self, vm, vb, vf):
        # TODO: what is the use of y?
        # arrange
        vm.loadl(0x200, 0x8cbe)
        vm.v[0xc] = vb

        # act
        vm.step()

        # assert
        assert vm.v[0xc] == 0xfe
        assert vm.v[0xf] == vf
        assert vm.pc == 0x202

    # Call opcode
    # TODO: could use msg check, but for now...
    def test_0nnn(self, vm):
        # arrange
        vm.loadl(0x200, 0x0123)

        # act & assert
        with pytest.raises(NotImplementedError):
            vm.step()

    # Conditional opcodes
    # TODO: need 2 tests -- equal and not equal
    def test_3xnn__vx_equals_nn(self, vm):
        # arrange
        vm.loadl(0x200, 0x3a11)
        vm.v[0xA] = 0x11

        # act
        vm.step()

        # assert
        vm.pc = 0x204

    def test_3xnn__vx_not_equals_nn(self, vm):
        # arrange
        vm.loadl(0x200, 0x3a11)
        vm.v[0xA] = 0x33

        # act
        vm.step()

        # assert
        vm.pc = 0x202

    def test_4xnn__vx_not_equals_nn(self, vm):
        # arrange
        vm.loadl(0x200, 0x4233)
        vm.v[0x2] = 0x35

        # act
        vm.step()

        # assert
        vm.pc = 0x204

    def test_4xnn__vx_equals_nn(self, vm):
        # arrange
        #vm = Chip8VirtualMachine()
        vm.loadl(0x200, 0x4233)
        vm.v[0x2] = 0x33

        # act
        vm.step()

        # assert
        vm.pc = 0x202

    def test_5xy0__vx_equals_vy(self, vm):
        # arrange
        vm.loadl(0x200, 0x5630)
        vm.v[0x6] = 0x14
        vm.v[0x3] = 0x14

        # act
        vm.step()

        # assert
        assert vm.pc == 0x204

    def test_5xy0__vx_not_equal_vy(self, vm):
        # arrange
        vm.loadl(0x200, 0x5630)
        vm.v[0x6] = 0x12
        vm.v[0x3] = 0x14

        # act
        vm.step()

        # assert
        assert vm.pc == 0x202


def test_9xy0__vx_not_equal_vy():
    # arrange
    vm = Chip8VirtualMachine()  # TODO: put in "provider" function
    vm.memory[0x200] = 0x96
    vm.memory[0x201] = 0x30
    vm.v[0x6] = 0x12
    vm.v[0x3] = 0x14

    # act
    vm.step()

    # assert
    assert vm.pc == 0x204


def test_9xy0__vx_equals_vy():
    # arrange
    vm = Chip8VirtualMachine()  # TODO: put in "provider" function
    vm.memory[0x200] = 0x96
    vm.memory[0x201] = 0x30
    vm.v[0x6] = 0x14
    vm.v[0x3] = 0x14

    # act
    vm.step()

    # assert
    assert vm.pc == 0x202


def test_6xnn():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x6a
    vm.memory[0x201] = 0xbc

    # act
    vm.step()

    # assert
    assert vm.v[0xa] == 0xbc
    assert vm.pc == 0x202


def test_7xnn():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x7e
    vm.memory[0x201] = 0xff
    vm.v[0xe] = 0xff

    # act
    vm.step()

    # assert
    assert vm.v[0xe] == 0xfe
    assert vm.pc == 0x202


# Display opcodes
def test_dxyn_put_0(vm, mocker):
    # arrange
    vm.loadl(0x200, 0xdab5)
    vm.v[0xa] = 0x00
    vm.v[0xb] = 0x00
    mocker.spy(vm.screen, "set")

    # act
    vm.step()

    # assert
    # TODO: not sure the order is correct according to spec
    assert vm.screen.set.call_args_list == [mocker.call(*t) for t in (
        (0, 0), (1, 0), (2, 0), (3, 0),
        (0, 1), (3, 1),
        (0, 2), (3, 2),
        (0, 3), (3, 3),
        (0, 4), (1, 4), (2, 4), (3, 4),
    )]

    assert vm.i == 0x0000       # no change
    assert vm.v[0xf] == 0x00    # no collision
    assert vm.pc == 0x202


def test_dxyn_put_0_with_wrap(vm, mocker):
    # arrange
    vm.loadl(0x200, 0xdab5)
    vm.v[0xa] = 62    # x
    vm.v[0xb] = 30    # y
    mocker.spy(vm.screen, "set")

    # act
    vm.step()

    # assert
    # TODO: not sure the order is correct according to spec -- wrap is in screen, not vm
    assert vm.screen.set.call_args_list == [mocker.call(*t) for t in (
        (62, 30), (63, 30), (64, 30), (65, 30),
        (62, 31), (65, 31),
        (62, 32), (65, 32),
        (62, 33), (65, 33),
        (62, 34), (63, 34), (64, 34), (65, 34),
    )]

    assert vm.i == 0x0000       # no change
    assert vm.v[0xf] == 0x00    # no collision
    assert vm.pc == 0x202


def test_dxyn_collision_test(vm, mocker):
    # arrange
    vm.loadl(0x200, 0xd311)
    vm.v[0x3] = 1    # x
    vm.v[0x1] = 1    # y
    vm.memory[0x0000] = 0b10000000
    vm.screen.set(1, 1)

    mocker.spy(vm.screen, "unset")

    # act
    vm.step()

    # assert
    assert vm.screen.unset.call_args_list == [mocker.call(1, 1)]
    assert vm.i == 0x0000       # no change
    assert vm.v[0xf] == 0x01    # collusion
    assert vm.pc == 0x202


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


# Flow opcodes
def test_00ee():
    # arrange
    vm = Chip8VirtualMachine()
    vm.pc = 0x300
    vm.stack = [0xaaa, 0x200]

    vm.memory[0x300] = 0x00
    vm.memory[0x301] = 0xee

    # act
    vm.step()

    # assert
    assert vm.pc == 0x200
    assert vm.stack == [0xaaa]


def test_1nnn():
    # command -- test modification
    # TODO: add "docstring"

    # arrange
    vm = Chip8VirtualMachine()

    # TODO: a "load" or "set" would be better: vm.memory.set(0x1a, 0xbc) or ('0x1abc')
    vm.memory[0x200] = 0x1a
    vm.memory[0x201] = 0xbc

    # act
    vm.step()

    # assert
    assert vm.pc == 0xabc


def test_2nnn():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x23
    vm.memory[0x201] = 0x45

    # act
    vm.step()

    # assert
    assert vm.pc == 0x345
    assert vm.stack == [0x200]


def test_bnnn():
    vm = Chip8VirtualMachine()
    vm.v[0x0] = 0xFF
    vm.memory[0x200] = 0xb3
    vm.memory[0x201] = 0x45

    # act
    vm.step()

    # assert
    vm.pc = 0x345 + 0xff
    # TODO: 0xfff + 0xff = 0x10fe -- overflow on memory (check that case)


# KeyOp opcodes
#def test_ex9e():
#    raise NotImplementedError


#def test_exa1():
#    raise NotImplementedError


#def test_fx0a():
#    raise NotImplementedError


# Math opcodes
def test_8xy4_without_carry():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x82
    vm.memory[0x201] = 0x84
    vm.v[0x2] = 0x10
    vm.v[0x8] = 0x20

    # act
    vm.step()

    # assert
    assert vm.v[0x2] == 0x30
    assert vm.v[0x8] == 0x20
    assert vm.v[0xf] == 0x00
    assert vm.pc == 0x202


def test_8xy4_with_carry():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x82
    vm.memory[0x201] = 0x84
    vm.v[0x2] = 0xff
    vm.v[0x8] = 0x20

    # act
    vm.step()

    # assert
    assert vm.v[0x2] == 0x1f
    assert vm.v[0x8] == 0x20
    assert vm.v[0xf] == 0x01
    assert vm.pc == 0x202


def test_8xy5_without_borrow():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x82
    vm.memory[0x201] = 0x85
    vm.v[0x2] = 0x0b
    vm.v[0x8] = 0x05

    # step
    vm.step()

    # assert
    assert vm.v[0x2] == 0x06
    assert vm.v[0x8] == 0x05
    assert vm.v[0xf] == 0x01    # no borrow
    assert vm.pc == 0x202


def test_8xy5_with_borrow():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x82
    vm.memory[0x201] = 0x85
    vm.v[0x2] = 0x0b
    vm.v[0x8] = 0x0c

    # step
    vm.step()

    # assert
    assert vm.v[0x2] == 0xfe    # guess TODO: verify
    assert vm.v[0x8] == 0x0c
    assert vm.v[0xf] == 0x00    # borrow
    assert vm.pc == 0x202


def test_8xy7_without_borrow():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x82
    vm.memory[0x201] = 0x87
    vm.v[0x2] = 0x11
    vm.v[0x8] = 0x20

    # step
    vm.step()

    # assert
    assert vm.v[0x2] == 0x0f
    assert vm.v[0x8] == 0x20
    assert vm.v[0xf] == 0x01    # no borrow
    assert vm.pc == 0x202


def test_8xy7_with_borrow():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0x82
    vm.memory[0x201] = 0x87
    vm.v[0x2] = 0x22
    vm.v[0x8] = 0x20

    # step
    vm.step()

    # assert
    assert vm.v[0x2] == 0xfd    # guess TODO: verify
    assert vm.v[0x8] == 0x20
    assert vm.v[0xf] == 0x00    # borrow
    assert vm.pc == 0x202


# Memory opcodes
def test_annn():
    # arrange
    vm = Chip8VirtualMachine()
    vm.memory[0x200] = 0xa1
    vm.memory[0x201] = 0x23

    # act
    vm.step()

    # assert
    assert vm.i == 0x123
    assert vm.pc == 0x202


def test_fx1e():
    # arrange
    vm = Chip8VirtualMachine()
    vm.loadl(0x200, 0xf31e)
    vm.v[0x3] = 0x44

    # act
    vm.step()

    # assert
    assert vm.v[0x3] == 0x44
    assert vm.i == 0x0044
    assert vm.pc == 0x202


def test_fx29():
    # arrange
    vm = Chip8VirtualMachine()
    vm.loadl(0x200, 0xf429)
    vm.v[0x4] = 0x3

    # act
    vm.step()

    # assert
    assert vm.i == 0x000f
    assert vm.pc == 0x202


def test_fx55():
    # arrange
    vm = Chip8VirtualMachine()
    vm.loadl(0x200, 0xf455)
    for offset, i in enumerate(range(0x05), start=0xA):
        vm.v[i] = offset
    vm.i = 0x250

    # act
    vm.step()

    # assert
    assert vm.i == 0x250
    assert vm.memory[0x250] == vm.v[0x0] == 0xa
    assert vm.memory[0x251] == vm.v[0x1] == 0xb
    assert vm.memory[0x252] == vm.v[0x2] == 0xc
    assert vm.memory[0x253] == vm.v[0x3] == 0xd
    assert vm.memory[0x254] == vm.v[0x4] == 0xe
    assert vm.pc == 0x202


def test_fx65():
    # arrange
    vm = Chip8VirtualMachine()
    vm.loadl(0x200, 0xf365)

    vm.i = 0x250
    vm.loadl(0x250, 0x1234, 0x5678)

    # act
    vm.step()

    # assert
    assert vm.pc == 0x202
    assert vm.i == 0x250
    assert vm.v[0x0] == vm.memory[0x250] == 0x12
    assert vm.v[0x1] == vm.memory[0x251] == 0x34
    assert vm.v[0x2] == vm.memory[0x252] == 0x56
    assert vm.v[0x3] == vm.memory[0x253] == 0x78


# Random opcodes
def test_cxnn(mocker):
    # arrange
    vm = Chip8VirtualMachine()
    vm.loadl(0x200, 0xc864)

    mocker.patch("random.randint").return_value = 0x25

    # act
    vm.step()

    # assert
    assert vm.v[0x8] == 0x24  # 0x25 & 0x64
    assert vm.pc == 0x202   # TODO: separate pc into (all that alter pc in expected way, and unexpected)


# Sound opcodes
def test_fx18():
    # arrange
    vm = Chip8VirtualMachine()
    vm.loadl(0x200, 0xf918)
    vm.v[0x9] = 0x25
    # TODO: add v out of bounds check

    # act
    vm.step()

    # assert
    assert vm.sound_timer_register == 0x25      # TODO: sound timer only goes down on next, right? and the sound?
    assert vm.v[0x9] == 0x25
    assert vm.pc == 0x202


# Timer opcodes
def test_fx07():
    # arrange
    vm = Chip8VirtualMachine()
    vm.loadl(0x200, 0xf507)
    vm.delay_timer_register = 0x33
    # TODO: add v out of bounds check

    # act
    vm.step()

    # assert
    assert vm.delay_timer_register == 0x33
    assert vm.v[0x5] == 0x33
    assert vm.pc == 0x202


def test_fx15():
    # arrange
    vm = Chip8VirtualMachine()
    vm.loadl(0x200, 0xfa15)
    vm.v[0xa] = 0xff
    # TODO: add v out of bounds check

    # act
    vm.step()

    # assert
    assert vm.delay_timer_register == 0xff
    assert vm.v[0xa] == 0xff
    assert vm.pc == 0x202


# TODO: should be in different file since this is an integration test (I think)
def test_with_file(vm):
    def load(fname):
        s = ""
        with open(fname) as f:
            for line in f:
                s += line   #.replace("\n", "")
        return s

    # arrange
    vm.loadf("Chip8 Picture.ch8")
    textshot = load("Chip8 Picture TEXTSHOT.txt")   # TODO: better if it was actual picture, but for now...

    # act
    vm.run(10000)

    # assert
    #print(vm.screen.screen)
    assert vm.screen.dump_textshot() == textshot
    #assert False