import pygame

import copy

from engine.gamescreen import GameScreen
from engine.input import Input
from engine.animation import Animation

class ScreenManager:
    def __init__(self, startScreen):
        self.currentScreen = startScreen
        self.currentScreen.load(self)
        self.currentScreen.setup()
        self.inp = Input()

        self.triangleWipe = pygame.image.load("data/images/transitions/Triangle Wipe.png").convert()
        self.triangleWipe.set_colorkey((0,0,0))
        
        self.screenWipeAnim = Animation([-320, 0, -320], 960, "Stop Restart", True, False)
        self.prevScreenWipeKeyframe = 0
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
        elif self.prevScreenWipeKeyframe != self.screenWipeAnim.index:
            if self.reloadingCurrent:
                self.reloadCurrentScreen()
                self.reloadingCurrent = False
            else:
                self.changeScreen(self.nextScreen)
                self.nextscreen = None
        
        self.prevScreenWipeKeyframe = self.screenWipeAnim.index

    def changeScreen(self, newScreen):
        del self.currentScreen
        self.currentScreen = newScreen
        self.currentScreen.load(self)
        self.currentScreen.setup()
    
    def changeScreenWithTransition(self, newScreen, speed=960):
        self.nextScreen = newScreen

        self.screenWipeAnim.speed = speed
        self.screenWipeAnim.start()
    
    def reloadCurrentScreen(self):
        self.currentScreen.load(self)
        self.currentScreen.setup()
    
    def reloadCurrentScreenWithTransition(self, speed=1280):
        self.reloadingCurrent = True
        
        self.screenWipeAnim.speed = speed
        self.screenWipeAnim.start()