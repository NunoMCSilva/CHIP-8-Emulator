from PIL import Image
import pytest

from chip8.vm import VirtualMachine, SimpleInfiniteLoop


@pytest.fixture
def vm():
    return VirtualMachine()


# TODO: refactor
class TestVirtualMachine:

    def _test_run__run_program__generate_expected_image(self, vm, program, expected_img):
        # arrange
        expected_img = Image.open(expected_img)
        vm.load_program(program)

        expected_data = list(expected_img.getdata())

        # act
        vm.run()

        # assert
        img = vm.screen.get_screenshot()
        #img.show()
        data = list(img.getdata())
        # TODO: why does this take so long when image is diff ?, ok, it's limited to PyCharm
        assert data == expected_data

    def test_run__chip8_picture__generates_expected_image(self, vm):
        # arrange
        program = "tests/integration/data/Chip8 Picture.ch8"
        expected_img = "tests/integration/data/Chip8 Picture.gif"

        # more arrange, then act and assert
        self._test_run__run_program__generate_expected_image(vm, program, expected_img)

    """
        # arrange
        expected_img = Image.open(program.replace(".ch8", ".gif"))
        vm.load_program(program)

        expected_data = list(expected_img.getdata())

        # act
        vm.run()

        # assert
        img = vm.screen.get_screenshot()
        img.show()
        data = list(img.getdata())
        # TODO: why does this take so long when image is diff ?, ok, it's limited to PyCharm
        assert data == expected_data
    """

    def test_run__random_number_test_with_exit_on_wait_keypress__generates_expected_image(self, mocker, vm):
        # arrange
        program = "tests/integration/data/Random Number Test [Matthew Mikolay, 2010].ch8"
        expected_img = "tests/integration/data/Random Number Test [Matthew Mikolay, 2010].gif"

        def mock_wait_for_keypress():
            raise SimpleInfiniteLoop

        mocker.patch.object(vm.keypad, "wait_for_keypress").side_effect = mock_wait_for_keypress
        mocker.patch("random.randint").return_value = 75

        # more arrange, then act and assert
        self._test_run__run_program__generate_expected_image(vm, program, expected_img)

    @pytest.mark.skip("issues with running -- takes too long on pytest")
    def test_123(self, vm):
        program = "tests/integration/data/SQRT Test [Sergey Naydenov, 2010].ch8"
        expected_img = "tests/integration/data/SQRT Test [Sergey Naydenov, 2010].gif"

        # more arrange, then act and assert
        self._test_run__run_program__generate_expected_image(vm, program, expected_img)



# TODO: will need some key and sound tests...
# TODO: and delay test...
