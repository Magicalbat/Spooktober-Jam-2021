import pygame

from engine.gamescreen import GameScreen
from engine.tilemap import Tilemap
from engine.particles import Particles
from engine.text import Text

from game.player import Player
from game.pumpkin import Pumpkin

class TestScreen(GameScreen):
    def setup(self):
        super().setup()

        self.tilemap = Tilemap(12)
        self.tilemap.loadFromJson("data/maps/test.json", True)

        self.player = Player(20, 100, 12, 12)

        self.pumpkins = []

        self.text = Text()
        self.text.loadFontImg("data/images/text.png", scale=(2,2))

        self.fps = 0

        #self.particles = Particles([8, 12], [-.1, .1, -.1, .1], [-25, 25, -45, -50], 1000, True, 4, 144, startCol=(0, 128, 128), endCol=(255, 255, 255))

    def draw(self, win):
        win.fill((200,200,200))

        self.tilemap.draw(win)
        #self.particles.draw(win)

        self.player.drawRect(win)
        
        for p in self.pumpkins:
            p.drawRect(win)

        win.blit(self.text.createTextSurf(str(self.fps)), (0,0))
        
        pygame.display.update()

    def update(self, delta, inp, fps=0):
        #self.particles.update(delta, self.tilemap.drawTiles, 1, 12)
        
        if delta:
            self.fps = int(1 / delta)
        delta = min(delta, 0.1)

        stillPumpkins = [p.rect for p in self.pumpkins if not p.handleCollision]

        self.player.update(delta, inp, stillPumpkins, self.tilemap.chunks)

        for p in self.pumpkins:
            p.update(delta, stillPumpkins, self.tilemap.chunks)

        if inp.keyJustPressed(pygame.K_f):
            self.pumpkins.append(Pumpkin(self.player.rect.x, self.player.rect.y, self.player.rect.w, self.player.rect.h, self.player.velocity, self.player.gravity))
            self.player.reset()

        #mousePos = pygame.mouse.get_pos()
        #self.particles.emit(mousePos, 2)