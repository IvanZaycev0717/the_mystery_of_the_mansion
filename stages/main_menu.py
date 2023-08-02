import pygame, sys
from settings import *
from math import sin
import os

path = os.path.dirname(os.path.abspath(__file__))
lang_file = 'lang.txt'
file_path = os.path.join(path, lang_file)

def lang_choise():
    with open(file_path, 'r') as file:
        return file.readline()
    
if lang_choise() == 'eng':
    from eng import *
elif lang_choise() == 'rus':
    from rus import *


class MainMenu:
    def __init__(self):
        
        # Imports your lang package
        lang_choise()

        # main setup
        self.display_surface = pygame.display.get_surface()

       

        # Font
        self.font = pygame.font.SysFont('arial', 38)

        
        # title and the mansion
        self.title_surf = pygame.image.load('images/main_menu/sc.png').convert_alpha()
        self.title_rect = self.title_surf.get_rect(centerx=WINDOW_WIDTH // 2 + 110, centery = WINDOW_HEIGHT // 2 - 85)

        # Moon
        self.moon_surf = pygame.image.load('images/main_menu/moon.png').convert_alpha()
        self.moon_rect = self.title_surf.get_rect(y=300)
        self.moon_offset = -150

        # Stars
        self.star_surf = pygame.image.load('images/main_menu/stars.jpg').convert()
        self.star_rect = self.star_surf.get_rect()
        self.star_offset = -150

        # Choices menu
        self.continue_button = self.font.render(CONTINUE_BUTTON, True, 'yellow')
        self.continue_button_rect = self.continue_button.get_rect(x=300, y=600)

    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def moving_moon(self, dt):
        self.moon_offset += dt * 400
        if -150 <= self.moon_offset <= 1050:
            self.moon_rect.x = int(self.moon_offset)
            self.moon_rect.y = 250 + sin((self.moon_rect.x + 150) * 0.0022) * -200
            self.display_surface.blit(self.moon_surf, self.moon_rect)
        else:
            self.display_surface.blit(self.moon_surf, self.moon_rect)
    
    def moving_stars(self, dt):
        self.star_offset += dt * 50
        if -150 <= self.star_offset <= 0:
            self.star_rect.x = int(self.star_offset)
            self.display_surface.blit(self.star_surf, self.star_rect)
        else:
            self.display_surface.blit(self.star_surf, self.star_rect)


    def run(self, dt):
        self.display_surface.fill(BLACK_GRAY)
        self.moving_stars(dt)
        self.moving_moon(dt)
        self.display_surface.blit(self.title_surf, self.title_rect)
        self.display_surface.blit(self.continue_button, self.continue_button_rect)
        
        self.event_loop()