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
        self.font_small = pygame.font.SysFont('arial', 20)

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

    # Language choice section
    def lang_choise(self):
        with open(file_path, 'r') as file:
            return file.readline()

    # Start screen section
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

    # Creation section
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
        lang = self.lang_choise()
        # Column 1
        self.esc_img = pygame.image.load('images/main_menu/esc.png').convert_alpha()
        self.esc_img_rect = self.esc_img.get_rect(x=10, y=10)
        

        self.right_button = pygame.image.load('images/main_menu/right.png').convert_alpha()
        self.right_button_rect = self.right_button.get_rect(x=10, y=50)

        self.left_button = pygame.image.load('images/main_menu/left.png').convert_alpha()
        self.left_button_rect = self.left_button.get_rect(x=10, y=90)


        self.save_button = pygame.image.load('images/main_menu/f5.png').convert_alpha()
        self.save_button_rect = self.save_button.get_rect(x=10, y=130)


        self.load_button = pygame.image.load('images/main_menu/f9.png').convert_alpha()
        self.load_button_rect = self.load_button.get_rect(x=10, y=170)
        

        self.esc_text = self.font_small.render(eng.MM_ESC if lang == 'eng' else rus.MM_ESC, False, 'yellow')
        self.esc_text_rect = self.esc_text.get_rect(x=60, y=15)
        

        self.right_text = self.font_small.render(eng.MM_RIGHT if lang == 'eng' else rus.MM_RIGHT, False, 'yellow')
        self.right_text_rect = self.right_text.get_rect(x=60, y=55)
        

        self.left_text = self.font_small.render(eng.MM_LEFT if lang == 'eng' else rus.MM_LEFT, False, 'yellow')
        self.left_text_rect = self.left_text.get_rect(x=60, y=95)
        

        self.f5_text = self.font_small.render(eng.MM_F5 if lang == 'eng' else rus.MM_F5, False, 'yellow')
        self.f5_text_rect = self.f5_text.get_rect(x=60, y=135)
        

        self.f9_text = self.font_small.render(eng.MM_F9 if lang == 'eng' else rus.MM_F9, False, 'yellow')
        self.f9_text_rect = self.f9_text.get_rect(x=60, y=175)
        

        # Column 2
        self.tab_img = pygame.image.load('images/main_menu/tab.png').convert_alpha()
        self.tab_img_rect = self.esc_img.get_rect(x=300, y=10)
        

        self.x_img = pygame.image.load('images/main_menu/x.png').convert_alpha()
        self.x_img_rect = self.x_img.get_rect(x=300, y=50)
        

        self.up_img = pygame.image.load('images/main_menu/up.png').convert_alpha()
        self.up_img_rect = self.up_img.get_rect(x=350, y=50)

        self.down_img = pygame.image.load('images/main_menu/down.png').convert_alpha()
        self.down_img_rect = self.down_img.get_rect(x=300, y=90)
        

        self.space_img = pygame.image.load('images/main_menu/space.png').convert_alpha()
        self.space_img_rect = self.space_img.get_rect(x=300, y=130)
        


        self.tab_text = self.font_small.render(eng.MM_TAB if lang == 'eng' else rus.MM_TAB, False, 'yellow')
        self.tab_text_rect = self.tab_text.get_rect(x=360, y=15)
        

        self.x_text = self.font_small.render(eng.MM_X if lang == 'eng' else rus.MM_X, False, 'yellow')
        self.x_text_rect = self.x_text.get_rect(x=400, y=55)
        

        self.down_text = self.font_small.render(eng.MM_DOWN if lang == 'eng' else rus.MM_DOWN, False, 'yellow')
        self.down_text_rect = self.down_text.get_rect(x=360, y=95)
        

        self.space_text = self.font_small.render(eng.MM_SPACE if lang == 'eng' else rus.MM_SPACE, False, 'yellow')
        self.space_text_rect = self.space_text.get_rect(x=530, y=135)
           

    # Show section
    def show_buttons(self):
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

    def show_controls(self):
        if self.control_panel_is_active:
            self.create_elemets_cp()
            self.control_panel_surf.fill(BLACK_GRAY)
            self.control_panel_surf.blit(self.esc_img, self.esc_img_rect)
            self.control_panel_surf.blit(self.right_button, self.right_button_rect)
            self.control_panel_surf.blit(self.left_button, self.left_button_rect)
            self.control_panel_surf.blit(self.save_button, self.save_button_rect)
            self.control_panel_surf.blit(self.load_button, self.load_button_rect)
            self.control_panel_surf.blit(self.esc_text, self.esc_text_rect)
            self.control_panel_surf.blit(self.right_text, self.right_text_rect)
            self.control_panel_surf.blit(self.left_text, self.left_text_rect)
            self.control_panel_surf.blit(self.f5_text, self.f5_text_rect)
            self.control_panel_surf.blit(self.f9_text, self.f9_text_rect)
            self.control_panel_surf.blit(self.tab_img, self.tab_img_rect)
            self.control_panel_surf.blit(self.x_img, self.x_img_rect)
            self.control_panel_surf.blit(self.up_img, self.up_img_rect)
            self.control_panel_surf.blit(self.down_img, self.down_img_rect)
            self.control_panel_surf.blit(self.space_img, self.space_img_rect)
            self.control_panel_surf.blit(self.tab_text, self.tab_text_rect)
            self.control_panel_surf.blit(self.x_text, self.x_text_rect)
            self.control_panel_surf.blit(self.down_text, self.down_text_rect)
            self.control_panel_surf.blit(self.space_text, self.space_text_rect) 
            self.display_surface.blit(self.control_panel_surf, self.control_panel_surf_rect)
    
    # Event section
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
    
    # Main cycle
    def run(self, dt):
        self.display_surface.fill(BLACK_GRAY)
        self.moving_stars(dt)
        self.moving_moon(dt)
        self.show_buttons()
        self.show_controls()

        self.event_loop()