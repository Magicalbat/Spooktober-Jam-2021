import pygame

def main():
    pygame.init()

    pygame.event.set_allowed([pygame.QUIT])

    width = 320
    height = 180
    win = pygame.display.set_mode((width, height), pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption('Spooktober Jam 2021')

    clock = pygame.time.Clock()
    fps = 60

    from engine.screenmanager import ScreenManager
    from game.testscreen import TestScreen

    screenManger = ScreenManager(TestScreen())

    running = True
    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        win.fill((200,200,200))
        screenManger.draw(win)
        pygame.display.update()

        screenManger.update(clock.get_time() / 1000)
        
    pygame.quit()

if __name__ == '__main__':
    main()