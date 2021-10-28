import pygame

import copy

from engine.entity import Entity

class Ghost(Entity):
    def __init__(self, x, y, width, height, yAccel):
        super().__init__(x, y, width, height, (200,200,200))

        self.img = pygame.image.load("data/images/characters/ghost.png").convert()
        self.img.set_colorkey((0,0,0))

        self.applyVelocity = True

        self.active = False

        self.moveDir = 1
        self.flipped = False
        self.speed = 12 * 6
        self.yAccel = yAccel

        self.finished = False
    
    def activate(self, pos, dir):
        self.pos = copy.deepcopy(pos)
        self.moveDir = dir
        self.flipped = not ((dir + 1) * .5)
        self.active = True
    
    def draw(self, win, scroll):
        if self.active:
            win.blit(pygame.transform.flip(self.img, self.flipped, False), (self.rect.x, self.rect.y))
            #super().drawRect(win, scroll)

    def update(self, delta):
        if self.active:
            self.velocity.x = self.speed * self.moveDir
            self.velocity.y -= self.yAccel * 0.01
        
            if self.pos.y < -24:
                self.finished = True
        
            super().update(delta)