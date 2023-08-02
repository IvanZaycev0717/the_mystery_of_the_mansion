import pygame, sys
from settings import *
from random import randint
from math import sin

class MainMenu:
    def __init__(self):

        # main setup
        self.display_surface = pygame.display.get_surface()
        

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
        
        self.event_loop()