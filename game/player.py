import pygame

import math, copy

from engine.entity import Entity

class Player(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (255,165,0))

        self.startPos = copy.deepcopy(self.pos)

        self.maxSpeed = 12 * 5
        self.accel = 12
        self.friction = 14

        self.jumpPressTimer = 0
        self.groundTimer = 0

        maxJumpHeight = 3.35 * 12
        minJumpHeight = 0.75 * 12
        jumpDur = 0.5

        self.gravity = 2 * maxJumpHeight / jumpDur ** 2
        self.maxJumpVel = -math.sqrt(2 * self.gravity * maxJumpHeight)
        self.minJumpVel = -math.sqrt(2 * self.gravity * minJumpHeight)

        self.applyGravity = True
        self.handleCollision = True
    
    def update(self, delta, inp, collisionRects=None, chunks=None):
        accelerating = False

        if inp.keyDown(pygame.K_RIGHT):
            self.velocity.x += self.accel
            self.velocity.x = min(self.velocity.x, self.maxSpeed)
            accelerating = True
        if inp.keyDown(pygame.K_LEFT):
            self.velocity.x -= self.accel
            self.velocity.x = max(self.velocity.x, -self.maxSpeed)
            accelerating = True
        
        moveDir = 0
        if self.velocity.x:
            moveDir = self.velocity.x / abs(self.velocity.x)

        if not accelerating:
            self.velocity.x -= self.friction * moveDir
            if moveDir == 1:
                self.velocity.x = max(self.velocity.x, 0)
            else:
                self.velocity.x = min(self.velocity.x, 0)

        super().update(delta, collisionRects, chunks)

        self.jumpPressTimer -= delta
        self.groundTimer -= delta

        if self.collisionTypes['bottom']:
            self.groundTimer = 0.1
        
        if inp.keyJustPressed(pygame.K_UP) or inp.keyJustPressed(pygame.K_c):
            self.jumpPressTimer = 0.05

        if self.groundTimer > 0 and self.jumpPressTimer > 0:
            self.velocity.y = self.maxJumpVel
            self.groundTimer = 0
            self.jumpPressTimer = 0
        
        if (inp.keyJustReleased(pygame.K_UP) or inp.keyJustReleased(pygame.K_c)) and self.velocity.y < self.minJumpVel:
            self.velocity.y = self.minJumpVel
    
    def reset(self):
        self.pos = copy.deepcopy(self.startPos)
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)
        self.velocity.x = 0
        self.velocity.y = 0