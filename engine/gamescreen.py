class GameScreen:
    def setup(self):
        pass

    def __init__(self):
        self.screenManager = None
        self.setup()
    
    def load(self, screenManager):
        self.screenManager = screenManager

    def draw(self, win):
        pass

    def update(self, delta, inp):
        pass