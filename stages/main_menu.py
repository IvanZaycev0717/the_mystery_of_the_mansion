import pygame, sys
from settings import *
from math import sin
import os
import eng
import rus

path = os.path.dirname(os.path.abspath(__file__))
lang_file = 'lang.txt'
file_path = os.path.join(path, lang_file)



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
        self.angle = 0
        

        # Stars
        self.star_surf = pygame.image.load('images/main_menu/stars.jpg').convert()
        self.star_rect = self.star_surf.get_rect()
        self.star_offset = -150

        # Mouse
        self.mouse_pos = pygame.mouse.get_pos()

        # Font
        self.font = pygame.font.SysFont('arial', 32)

        # Main Menu Button Surfaces
        self.continie_surf = pygame.Surface((MM_BUTTON_W, MM_BUTTON_H))
        self.continie_surf.fill(BLACK_GRAY)
        self.continie_surf_rect = self.continie_surf.get_rect(x=850, y=450)

        self.new_game_surf = pygame.Surface((MM_BUTTON_W, MM_BUTTON_H))
        self.new_game_surf.fill(BLACK_GRAY)
        self.new_game_surf_rect = self.new_game_surf.get_rect(x=850, y=500)

        self.controls_surf = pygame.Surface((MM_BUTTON_W, MM_BUTTON_H))
        self.controls_surf.fill(BLACK_GRAY)
        self.controls_surf_rect = self.controls_surf.get_rect(x=850, y=550)

        self.settings_surf = pygame.Surface((MM_BUTTON_W, MM_BUTTON_H))
        self.settings_surf.fill(BLACK_GRAY)
        self.settings_surf_rect = self.settings_surf.get_rect(x=850, y=600)

        self.exit_surf = pygame.Surface((MM_BUTTON_W, MM_BUTTON_H))
        self.exit_surf.fill(BLACK_GRAY)
        self.exit_surf_rect = self.exit_surf.get_rect(x=850, y=650)

        # Control panel
        self.control_panel_surf = pygame.Surface((725, 235))
        self.control_panel_surf.fill(BLACK_GRAY)
        self.control_panel_surf_rect = self.control_panel_surf.get_rect(x=50, y=450)
        self.control_panel_is_active = False

    def lang_choise(self):
        with open(file_path, 'r') as file:
            return file.readline()

    def button_creation(self):
        # Choices menu
        lang = self.lang_choise()
        self.continue_button = self.font.render(eng.CONTINUE_BUTTON if lang == 'eng' else rus.CONTINUE_BUTTON, True, 'gray')
        self.continue_button_rect = self.continue_button.get_rect(x=875, y=450)
        self.new_game_button = self.font.render(eng.NEW_GAME_BUTTON if lang == 'eng' else rus.NEW_GAME_BUTTON, True, 'yellow')
        self.new_game_button_rect = self.new_game_button.get_rect(x=875, y=500)
        self.controls_button = self.font.render(eng.CONTROLS_BUTTON if lang == 'eng' else rus.CONTROLS_BUTTON, True, 'yellow')
        self.controls_rect = self.controls_button.get_rect(x=875, y=550)
        self.settings_button = self.font.render(eng.SETTINGS_BUTTON if lang == 'eng' else rus.SETTINGS_BUTTON, True, 'yellow')
        self.settings_rect = self.settings_button.get_rect(x=875, y=600)
        self.quit_button = self.font.render(eng.QUIT_BUTTON if lang == 'eng' else rus.QUIT_BUTTON, True, 'yellow')
        self.quit_rect = self.quit_button.get_rect(x=875, y=650)

    def create_elemets_cp(self):
        self.esc_img = pygame.image.load('images/main_menu/esc.png').convert_alpha()
        self.esc_img_rect = self.esc_img.get_rect(x=10, y=10)
        self.control_panel_surf.blit(self.esc_img, self.esc_img_rect)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                self.continie_surf.fill(MM_BUT_COLOR) if self.continie_surf_rect.collidepoint(event.pos) else self.continie_surf.fill(BLACK_GRAY)
                self.new_game_surf.fill(MM_BUT_COLOR) if self.new_game_surf_rect.collidepoint(event.pos) else self.new_game_surf.fill(BLACK_GRAY)
                self.controls_surf.fill(MM_BUT_COLOR) if self.controls_surf_rect.collidepoint(event.pos) else self.controls_surf.fill(BLACK_GRAY)
                self.settings_surf.fill(MM_BUT_COLOR) if self.settings_surf_rect.collidepoint(event.pos) else self.settings_surf.fill(BLACK_GRAY)
                self.exit_surf.fill(MM_BUT_COLOR) if self.exit_surf_rect.collidepoint(event.pos) else self.exit_surf.fill(BLACK_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN and self.exit_surf_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.controls_surf_rect.collidepoint(event.pos):
                self.control_panel_is_active = True if not self.control_panel_is_active else False
    
    def show_control_panel(self):
        self.display_surface.blit(self.control_panel_surf, self.control_panel_surf_rect)

    def moving_moon(self, dt):
        self.moon_offset += dt * 400
        self.rotated_moon = pygame.transform.rotate(self.moon_surf, self.angle)
        self.rotated_moon_rect = self.rotated_moon.get_rect(center=(self.moon_rect.x + 50, self.moon_rect.y + 50))
        if -150 <= self.moon_offset <= 1050:
            self.moon_rect.x = int(self.moon_offset)
            self.moon_rect.y = 250 + sin((self.moon_rect.x + 150) * 0.0022) * - 200
            self.display_surface.blit(self.moon_surf, self.moon_rect)
        else:
            self.moon_offset = 1051
            self.display_surface.blit(self.rotated_moon, self.rotated_moon_rect)
            if self.angle > -5000:
                self.angle -= 0.2
            else:
                self.angle = 0

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
        self.display_surface.blit(self.continie_surf, self.continie_surf_rect)
        self.display_surface.blit(self.new_game_surf, self.new_game_surf_rect)
        self.display_surface.blit(self.controls_surf, self.controls_surf_rect)
        self.display_surface.blit(self.settings_surf, self.settings_surf_rect)
        self.display_surface.blit(self.exit_surf, self.exit_surf_rect)
        self.button_creation()
        self.display_surface.blit(self.title_surf, self.title_rect)
        self.display_surface.blit(self.continue_button, self.continue_button_rect)
        self.display_surface.blit(self.new_game_button, self.new_game_button_rect)
        self.display_surface.blit(self.controls_button, self.controls_rect)
        self.display_surface.blit(self.settings_button, self.settings_rect)
        self.display_surface.blit(self.quit_button, self.quit_rect)
        if self.control_panel_is_active:
            self.show_control_panel()
            self.create_elemets_cp()
        self.event_loop()