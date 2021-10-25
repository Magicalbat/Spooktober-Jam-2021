import pygame

import math, copy

from engine.entity import Entity

class Player(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (255,165,0))

        self.startPos = copy.deepcopy(self.pos)

        self.speed = 12 * 4

        maxJumpHeight = 3.25 * 12
        minJumpHeight = 0.75 * 12
        jumpDur = 0.5

        self.gravity = 2 * maxJumpHeight / jumpDur ** 2
        self.maxJumpVel = -math.sqrt(2 * self.gravity * maxJumpHeight)
        self.minJumpVel = -math.sqrt(2 * self.gravity * minJumpHeight)

        self.applyGravity = True
        self.handleCollision = True
    
    def update(self, delta, inp, collisionRects=None, chunks=None):
        self.velocity.x = 0

        if inp.keyDown(pygame.K_d):
            self.velocity.x = self.speed
        if inp.keyDown(pygame.K_a):
            self.velocity.x = -self.speed
        
        super().update(delta, collisionRects, chunks)

        if self.collisionTypes['bottom'] and (inp.keyJustPressed(pygame.K_UP) or inp.keyJustPressed(pygame.K_SPACE) or inp.keyJustPressed(pygame.K_w)):
            self.velocity.y = self.maxJumpVel
        
        if (inp.keyJustReleased(pygame.K_UP) or inp.keyJustReleased(pygame.K_SPACE) or inp.keyJustReleased(pygame.K_w)) and self.velocity.y < self.minJumpVel:
            self.velocity.y = self.minJumpVel
    
    def reset(self):
        self.pos = copy.deepcopy(self.startPos)
        self.velocity.x = 0
        self.velocity.y = 0