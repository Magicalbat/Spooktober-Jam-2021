from engine.gamescreen import GameScreen
from engine.input import Input

class ScreenManager:
    def __init__(self, startScreen):
        self.currentScreen = startScreen
        self.currentScreen.load(self)
        self.inp = Input()
    
    def draw(self, win):
        self.currentScreen.draw(win)

    def update(self, delta):
        self.inp.update()
        self.currentScreen.update(delta, self.inp)

    def changeScreen(self, newScreen):
        del self.currentScreen
        self.currentScreen = newScreen
        self.currentScreen.load(self)
    
    def reloadCurrentScreen(self):
        self.currentScreen.setup()
        self.currentScreen.load(self)