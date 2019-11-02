



"""
    @pytest.mark.parametrize("program", [
        #"tests/integration/data/Chip8 Picture.ch8",
        "tests/integration/data/Random Number Test [Matthew Mikolay, 2010].ch8" # TODO: -- bug: seems to see 0xf090 (hex data) as opcode
        # this one will need mocker.random.randint
    ])
    def test_chip8_picture(self, vm, program):
        # arrange
        expected_img = Image.open(program.replace(".ch8", ".gif"))
        vm.load_program(program)

        expected_data = list(expected_img.getdata())

        # act
        vm.run()

        # assert
        img = vm.screen.get_screenshot()
        data = list(img.getdata())
        # TODO: why does this take so long when image is diff ?, ok, it's limited to PyCharm
        assert data == expected_data


# TODO: should be in different file since this is an integration test (I think)
@pytest.mark.skip
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
"""
