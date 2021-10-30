import sys

import pygame

from engine.gamescreen import GameScreen
from engine.menu import Menu
from game.controlsscreen import ControlsScreen
from game.creditsscreen import CreditsScreen
from game.level import Level

class StartScreen(GameScreen):
    def quit(self):
        pygame.quit()
        sys.exit()

    def load(self, screenManager):
        GameScreen.load(self, screenManager)
        self.menu = Menu(["Start", "Controls", "Credits", "Exit"], 3, (0, 35), (15, 25), \
            {0:screenManager.changeScreenWithTransition, 1:screenManager.changeScreenWithTransition, 2:screenManager.changeScreenWithTransition, 3:self.quit},\
                 {0:Level(prevScreen=self), 1:ControlsScreen(prevScreen=self), 2:CreditsScreen(prevScreen=self)}, (255, 229, 127))

    def draw(self, win):
        self.menu.draw(win)

    def update(self, delta, inp):
        self.menu.update(inp, delta)