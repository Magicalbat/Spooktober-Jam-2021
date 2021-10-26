import pygame

pygame.init()

pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEWHEEL])

width = int(320 * 1.5)
height = int(180 * 1.5)
screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.RESIZABLE, 16)
pygame.display.set_caption("Level Editor V2")

clock = pygame.time.Clock()
fps = 60

import enum

from engine.common import *
from engine.input import Input
from engine.tilemap import Tilemap
from engine.text import Text

class editStates(enum.Enum):
    PENCIL = enum.auto(),
    BOX_SELECT = enum.auto(),
    BUCKET = enum.auto(),
    COLOR_PICKER = enum.auto()

def changeEditState(oldState, newState, changeCursor=True):
    oldState = newState

    if changeCursor:
        if newState == editStates.PENCIL:
            setCursorFromTxt("levelEditor/data/pencil.txt")
        elif newState == editStates.BOX_SELECT:
            setCursorFromTxt("levelEditor/data/box select.txt")
        elif newState == editStates.BUCKET:
            setCursorFromTxt("levelEditor/data/bucket.txt")
        elif newState == editStates.COLOR_PICKER:
            setCursorFromTxt("levelEditor/data/color picker.txt")

tileSize = 12
tilemap = Tilemap(tileSize, layers=2)
tilemap.loadTileImgs("data/images/tiles/tiles.png", (4,4), (1, 1), 16, (0, 0, 0))

tilemap.loadFromJson("data/maps/level1.json", True)

editLayer = 0
editState = 0
changeEditState(editState, editStates.PENCIL)
selectedTile = 0

tileImgs = loadSpriteSheet("data/images/tiles/tiles.png", (12,12), (4,4), (1, 1), 16, (0, 0, 0))

sbWidth = int(tileSize * 5) # sidebar width
sidebar = pygame.Surface((sbWidth, height))

sbScroll = tileSize * 3
sbScrollSpeed = tileSize
sbTileRects = [pygame.Rect((tileSize + (2 * tileSize * (i % 2)), sbScroll + ((i // 2) * 2 * tileSize), tileSize, tileSize)) for i in range(len(tileImgs))]

win = pygame.Surface((width - sbWidth, height))

scroll = [0,0]
scrollSpeed = tileSize * 10

text = Text()
text.loadFontImg("data/images/text.png")#, scale=(2,2))

inp = Input()

running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            if mousePos[0] < sbWidth:
                sbScroll += sbScrollSpeed * event.y

                sbTileRects = [pygame.Rect((tileSize + (2 * tileSize * (i % 2)), sbScroll + ((i // 2) * 2 * tileSize), tileSize, tileSize)) for i in range(len(tileImgs))]

    delta = clock.get_time() / 1000

    inp.update()

    # CHANGE EDIT STATES ===============================
    if inp.keyJustPressed(pygame.K_p):
        changeEditState(editState, editStates.PENCIL)
    if inp.keyJustPressed(pygame.K_e):
        changeEditState(editState, editStates.BOX_SELECT)
    if inp.keyJustPressed(pygame.K_f):
        changeEditState(editState, editStates.BUCKET)
    if inp.keyJustPressed(pygame.K_k):
        changeEditState(editState, editStates.COLOR_PICKER)
    
    # CAMERA MOVEMENT ===================================
    if inp.keyDown(pygame.K_w):
        scroll[1] -= scrollSpeed * delta
    if inp.keyDown(pygame.K_a):
        scroll[0] -= scrollSpeed * delta
    if inp.keyDown(pygame.K_s):
        scroll[1] += scrollSpeed * delta
    if inp.keyDown(pygame.K_d):
        scroll[0] += scrollSpeed * delta
    
    if inp.keyJustPressed(pygame.K_PERIOD):
        scroll = [0,0]
    
    mousePos = pygame.mouse.get_pos()
    tileMousePos = (mousePos[0] // tileSize, mousePos[1] // tileSize)
    scrolledTileMousePos = ((mousePos[0] - scroll[0]) // tileSize, (mousePos[1] - scroll[1]) // tileSize)
    clampedMousePos = (tileMousePos[0] * tileSize, tileMousePos[1] * tileSize)

    if mousePos[0] < sbWidth: # SIDEBAR LOGIC ==========
        if inp.mouseJustPressed(0):
            for i in range(len(sbTileRects)):
                if sbTileRects[i].collidepoint(mousePos):
                    selectedTile = i
                    break
    else: # WIN LOGIC =================================
        pass

    # WIN DRAW =========================================
    win.fill((200,200,200))

    tilemap.draw(win, scroll)

    win.blit(tileImgs[selectedTile], (clampedMousePos[0] - sbWidth, clampedMousePos[1]))
    pygame.draw.rect(win, (0,245,255), (clampedMousePos[0] - sbWidth - 1, clampedMousePos[1] - 1, tileSize+2, tileSize+2), width=1)

    pygame.draw.rect(win, (255,255,255), (-scroll[0], -scroll[1], 320, 180), width=1)

    # SIDEBAR DRAW =====================================
    sidebar.fill((50,50,75))

    for i in range(len(tileImgs)):
        sidebar.blit(tileImgs[i], (tileSize + (2 * tileSize * (i % 2)), sbScroll + ((i // 2) * 2 * tileSize)))
    
    sRect = sbTileRects[selectedTile] # Selected Rect
    pygame.draw.rect(sidebar, (0,245,255), (sRect.x - 1, sRect.y - 1, sRect.w + 2, sRect.h + 2), width=1)

    pygame.draw.rect(sidebar, (50,50,75), (0,0,sbWidth,20))

    sidebar.blit(text.createTextSurf(f"Layer: {editLayer}"), (0,0))
    sidebar.blit(text.createTextSurf(f"({int(clampedMousePos[0])}, {int(clampedMousePos[1])})"), (0,9))
    sidebar.blit(text.createTextSurf(f"({int(scrolledTileMousePos[0])}, {int(scrolledTileMousePos[1])})"), (0,18))

    screen.blit(win, (sbWidth, 0))
    screen.blit(sidebar, (0,0))
    pygame.display.update()

pygame.quit()