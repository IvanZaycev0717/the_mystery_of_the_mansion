import pygame, sys


from settings import *
from author import Author


class Main:
    def __init__(self):
        # Game window setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.title = pygame.display.set_caption(TITLE)
        self.icon = pygame.display.set_icon(pygame.image.load(ICON_PATH).convert_alpha())

        # Class objects
        self.author_screen = Author()

        # Stages
        self.stage = 1


    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.stage = 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.stage = 2
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.stage = 3
            
            # Switching stages
            if self.stage == 1:
                self.stage = self.author_screen.run()
            elif self.stage == 2:
                self.display_surface.fill('pink')
            elif self.stage == 3:
                self.display_surface.fill('brown')
            print(self.stage)
            

            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()