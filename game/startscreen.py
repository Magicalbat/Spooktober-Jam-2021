import sys

import pygame

from engine.gamescreen import GameScreen
from game.level import Level
from engine.menu import Menu

class StartScreen(GameScreen):
    def setup(self):
        self.menu = None
    
    def quit(self):
        pygame.quit()
        sys.exit()

    def load(self, screenManager):
        GameScreen.load(self, screenManager)
        self.menu = Menu(["Start", "Options", "Exit"], 4, (0, 50), (25, 25), {0:screenManager.changeScreenWithTransition, 2:self.quit}, {0:Level()})

    def draw(self, win):
        self.menu.draw(win)

    def update(self, delta, inp):
        self.menu.update(inp, delta)