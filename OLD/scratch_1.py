"""
        #img.save("test.bmp")
        #j = Image.open("tests/integration/data/Chip8 Picture.gif")

        #print(list(img.getdata()))
        #print(list(j.getdata()))
        #assert list(img.getdata()) == list(j.getdata())


        # img.show()


        i = Image.open("test.bmp")
        print(i)

        #k = Image.open("tests/integration/data/Chip8 Picture.bmp")
        print(j)
        print(i == j)

        print(len(i.getdata()))
        print(len(j.getdata()))

        print(i.getdata())
        assert list(i.getdata()) == list(j.getdata())

        raise NotImplementedError

    ""
    def dump_textshot(self) -> str:
        # a screenshot representation...
        s = ""
        for y in range(self.y_size):
            for x in range(self.x_size):
                s += "X" if self.get(x, y) == 1 else " "
            s += "\n"
        return s
    ""
"""