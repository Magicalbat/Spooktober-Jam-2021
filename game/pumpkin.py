import pygame

import copy

from engine.entity import Entity

class Pumpkin(Entity):
    def __init__(self, x, y, width, height, startVel, gravity, img):
        super().__init__(x, y, width, height, (0,255,0))

        self.velocity = copy.deepcopy(startVel)
        self.gravity = copy.deepcopy(gravity)

        self.applyGravity = True
        self.handleCollision = True
        self.applyVelocity = True

        self.stopping = False

        self.img = img
    
    def draw(self, win, scroll=(0,0)):
        #super().drawRect(win, scroll)
        win.blit(self.img, (self.rect.x - scroll[0] - 1, self.rect.y - scroll[1] - 2))
    
    def update(self, delta, collisionRects=None, chunks=None):
        rects = copy.deepcopy(collisionRects)
        if self.rect in collisionRects:
            rects.remove(self.rect)
        super().update(delta, rects, chunks)

        if self.velocity.y == 0:
            self.stopping = True

            self.applyGravity = False
            self.handleCollision = False

            self.velocity.x = 0
            self.velocity.y = 0