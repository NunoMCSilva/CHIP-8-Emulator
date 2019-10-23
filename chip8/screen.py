from PIL import Image, ImageDraw
# TODO: import error -- doesn't allow screenshot


# TODO: more like MockScreen, but... check model based testing
class Screen:
    # 64 x 32 pixels

    def __init__(self, width=64, height=32):    #, screen_set=None, screen_unset=None):
        self.screen = {}    # TODO: can replaced with set
        self.width = width
        self.height = height
        #self.screen_set = screen_set
        #self.screen_unset = screen_unset

    def clear(self):
        # clear screen
        self.screen = {}

    """
    # TODO: check, experimental
    def draw_sprite(self, x, y, sprite) -> bool:
        ""
        Draw a sprite at position VX, VY with N bytes of sprite data starting at the address stored in I
Set VF to 01 if any set pixels are changed to unset, and 00 otherwise
        # rets collided
        ""
        pass
    """

    def get(self, x, y):
        return self.screen.get((x % self.width, y % self.height), 0)

    def unset(self, x, y):
        self.screen[(x % self.width, y % self.height)] = 0
        #if self.screen_unset is not None:
            #self.screen_unset(x, y)

    def set(self, x, y):
        self.screen[(x, y)] = 1
        #if self.screen_set is not None:
            #self.screen_set(x, y)

    def get_screenshot(self) -> Image:
        img = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        for x, y in self.screen:
            draw.point((x, y), 1)

        return img
