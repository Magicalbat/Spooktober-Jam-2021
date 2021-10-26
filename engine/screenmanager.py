import pygame

from engine.gamescreen import GameScreen
from engine.input import Input
from engine.animation import Animation

class ScreenManager:
    def __init__(self, startScreen):
        self.currentScreen = startScreen
        self.currentScreen.load(self)
        self.inp = Input()

        self.triangleWipe = pygame.image.load("data/images/transitions/Triangle Wipe.png").convert()
        self.triangleWipe.set_colorkey((0,0,0))
        
        self.screenWipeAnim = Animation([-320, 0, -320], 320 * 3, "Stop Restart", True, False)
        self.nextScreen = None
        self.reloadingCurrent = False
    
    def draw(self, win):
        self.currentScreen.draw(win)

        if self.screenWipeAnim.active:
            win.blit(self.triangleWipe, (self.screenWipeAnim.value, 0))

    def update(self, delta):
        self.inp.update()
        self.screenWipeAnim.update(delta)

        if not self.screenWipeAnim.active:
            self.currentScreen.update(delta, self.inp)
        elif abs(self.screenWipeAnim.value) < 10:
            if self.reloadingCurrent:
                self.reloadCurrentScreen()
                self.reloadingCurrent = False
            else:
                self.changeScreen(self.nextScreen)
                self.nextscreen = None

    def changeScreen(self, newScreen):
        del self.currentScreen
        self.currentScreen = newScreen
        self.currentScreen.load(self)
    
    def changeScreenWithTransition(self, newScreen):
        self.nextScreen = newScreen
        self.screenWipeAnim.start()
    
    def reloadCurrentScreen(self):
        self.currentScreen.setup()
        self.currentScreen.load(self)
    
    def reloadCurrentScreenWithTransition(self):
        self.reloadingCurrent = True
        self.screenWipeAnim.start()