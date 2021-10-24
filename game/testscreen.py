import pygame

from engine.gamescreen import GameScreen

class TestScreen(GameScreen):
    def setup(self):
        super().setup()

    def draw(self, win):
        win.fill((200,200,200))

        pygame.display.update()

    def update(self, delta, inp):
        pass