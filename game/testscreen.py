import pygame

from engine.gamescreen import GameScreen
from engine.tilemap import Tilemap
from engine.particles import Particles
from engine.text import Text
from engine.common import *

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

        self.scroll = [0,0]
        self.cameraBounds = ((0,0),(0,0))

        #self.particles = Particles([8, 12], [-.1, .1, -.1, .1], [-25, 25, -45, -50], 1000, True, 4, 144, startCol=(0, 128, 128), endCol=(255, 255, 255))

    def draw(self, win):
        self.scroll[0] += ((self.player.pos.x - win.get_width() / 2) - self.scroll[0]) / 20
        
        self.scroll[0] = clamp(self.scroll[0], self.cameraBounds[0][0], self.cameraBounds[0][1])
        
        self.scroll[1] += ((self.player.pos.y - win.get_height() / 2) - self.scroll[1]) / 20
        
        self.scroll[1] = clamp(self.scroll[1], self.cameraBounds[1][0], self.cameraBounds[1][1])

        win.fill((200,200,200))

        self.tilemap.draw(win, self.scroll)
        #self.particles.draw(win)

        self.player.drawRect(win, self.scroll)
        
        for p in self.pumpkins:
            p.drawRect(win, self.scroll)

        win.blit(self.text.createTextSurf(f'{self.fps}'), (0,0))
        
        pygame.display.update()

    def update(self, delta, inp, fps=0):
        #self.particles.update(delta, self.tilemap.drawTiles, 1, 12)
        
        if delta:
            self.fps = int(1 / delta)
        delta = min(delta, 0.1)

        entityRects = [p.rect for p in self.pumpkins]

        self.player.update(delta, inp, entityRects, self.tilemap.chunks)

        entityRects.append(self.player.rect)

        for p in self.pumpkins:
            p.update(delta, entityRects, self.tilemap.chunks)

        if inp.keyJustPressed(pygame.K_x):
            self.pumpkins.append(Pumpkin(self.player.rect.x, self.player.rect.y, self.player.rect.w, self.player.rect.h, self.player.velocity, self.player.gravity))
            
            self.player.reset()

            hitlist = getCollidingRects(self.player.rect, [p.rect for p in self.pumpkins])
            
            for rect in hitlist:
                self.pumpkins.remove(rect)

        if inp.keyJustPressed(pygame.K_r):
            self.screenManager.reloadCurrentScreen()

        #mousePos = pygame.mouse.get_pos()
        #self.particles.emit(mousePos, 2)