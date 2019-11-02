class Model:

    def __init__(self):
        print("self.vm = chip8_.chip8.vm()")
        self.key_pressed = None

    def on_keypress(self, key):
        self.key_pressed = key

    def on_step(self):
        self.key_pressed = None
        print("self.vm.step()")
