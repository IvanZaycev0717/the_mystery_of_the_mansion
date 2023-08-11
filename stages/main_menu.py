from math import sin
import os
import sys

import pygame


import eng
import rus
from img_imports import import_folder_dict
from settings import *

path = os.path.dirname(os.path.abspath(__file__))
lang_file = 'lang.txt'
file_path = os.path.join(path, lang_file)


class MainMenu:
    def __init__(self):

        # main setup
        self.display_surface = pygame.display.get_surface()

        # Main menu image imports
        self.main_menu_dct = import_folder_dict('images/main_menu/')

        # title and the mansion
        self.title_rect = self.main_menu_dct['sc'].get_rect(centerx=WINDOW_WIDTH // 2 + 110, centery = WINDOW_HEIGHT // 2 - 85)

        # Moon
        self.moon_rect = self.main_menu_dct['moon'].get_rect(y=300)
        self.moon_offset = -150
        self.angle = 0

        # Lang
        self.current_lang = 'eng'

        # Next stage toggle
        self.next_stage = None
        

        # Stars
        self.star_rect = self.main_menu_dct['stars'].get_rect()
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

        # Controls imports
        # Rectangles for controls
        self.esc_img_rect = self.main_menu_dct['esc'].get_rect(x=10, y=10)
        self.right_button_rect = self.main_menu_dct['right'].get_rect(x=10, y=50)
        self.left_button_rect = self.main_menu_dct['left'].get_rect(x=10, y=90)
        self.save_button_rect = self.main_menu_dct['f5'].get_rect(x=10, y=130)
        self.load_button_rect = self.main_menu_dct['f9'].get_rect(x=10, y=170)
        self.tab_img_rect = self.main_menu_dct['tab'].get_rect(x=300, y=10)
        self.x_img_rect = self.main_menu_dct['x'].get_rect(x=300, y=50)
        self.up_img_rect = self.main_menu_dct['up'].get_rect(x=350, y=50)
        self.down_img_rect = self.main_menu_dct['down'].get_rect(x=300, y=90)
        self.space_img_rect = self.main_menu_dct['space'].get_rect(x=300, y=130)

        # Settings panel
        self.settings_panel_surf = pygame.Surface((725, 235))
        self.settings_panel_surf.fill(BLACK_GRAY)
        self.settings_panel_surf_rect = self.control_panel_surf.get_rect(x=50, y=450)
        self.settings_panel_is_active = False


        # toggle lang
        self.change_eng_surf = pygame.Surface((150, 40))
        self.change_eng_surf_rect = self.change_eng_surf.get_rect(x=70, y=500)
        self.change_eng_surf.fill(MM_BUT_COLOR)

        self.change_rus_surf = pygame.Surface((150, 40))
        self.change_rus_surf_rect = self.change_eng_surf.get_rect(x=230, y=500)
        self.change_rus_surf.fill(MM_BUT_COLOR)

        self.frame_1 = pygame.draw.rect(self.settings_panel_surf, MM_BUT_COLOR, (10, 10, 375, 90), 3)
        self.frame_2 = pygame.draw.rect(self.settings_panel_surf, MM_BUT_COLOR, (10, 120, 375, 90), 3)
        self.frame_3 = pygame.draw.rect(self.settings_panel_surf, MM_BUT_COLOR, (400, 10, 310, 90), 3)
        self.frame_4 = pygame.draw.rect(self.settings_panel_surf, MM_BUT_COLOR, (400, 120, 310, 90), 3)
        self.lang_helper = self.font_small.render('Click your language / Кликните на ваш язык', False, 'yellow')
        self.eng_lang = self.font.render('English', False, 'yellow')
        self.rus_lang = self.font.render('Русский', False, 'yellow')
        self.lang_helper_rect = self.lang_helper.get_rect(x=30, y=20)
        self.eng_lang_rect = self.eng_lang.get_rect(x=30, y=50)
        self.rus_lang_rect = self.rus_lang.get_rect(x=190, y=50)


    # Language choice section
    def lang_choise(self):
        with open(file_path, 'r') as file:
            self.current_lang = file.readline()
            return self.current_lang

    def toggle_lang(self, lang):
        with open(file_path, 'w') as file:
            file.write(lang)
            self.current_lang = lang

    # Start screen section
    def moving_moon(self, dt):
        self.moon_offset += dt * 400
        self.rotated_moon = pygame.transform.rotate(self.main_menu_dct['moon'], self.angle)
        self.rotated_moon_rect = self.rotated_moon.get_rect(center=(self.moon_rect.x + 50, self.moon_rect.y + 50))
        if -150 <= self.moon_offset <= 1050:
            self.moon_rect.x = int(self.moon_offset)
            self.moon_rect.y = 250 + sin((self.moon_rect.x + 150) * 0.0022) * - 200
            self.display_surface.blit(self.main_menu_dct['moon'], self.moon_rect)
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
            self.display_surface.blit(self.main_menu_dct['stars'], self.star_rect)
        else:
            self.display_surface.blit(self.main_menu_dct['stars'], self.star_rect)

    # Creation section
    def button_creation(self):
        # Choices menu
        self.continue_button = self.font.render(eng.CONTINUE_BUTTON if self.current_lang == 'eng' else rus.CONTINUE_BUTTON, True, 'gray')
        self.continue_button_rect = self.continue_button.get_rect(x=875, y=450)
        self.new_game_button = self.font.render(eng.NEW_GAME_BUTTON if self.current_lang == 'eng' else rus.NEW_GAME_BUTTON, True, 'yellow')
        self.new_game_button_rect = self.new_game_button.get_rect(x=875, y=500)
        self.controls_button = self.font.render(eng.CONTROLS_BUTTON if self.current_lang == 'eng' else rus.CONTROLS_BUTTON, True, 'yellow')
        self.controls_rect = self.controls_button.get_rect(x=875, y=550)
        self.settings_button = self.font.render(eng.SETTINGS_BUTTON if self.current_lang == 'eng' else rus.SETTINGS_BUTTON, True, 'yellow')
        self.settings_rect = self.settings_button.get_rect(x=875, y=600)
        self.quit_button = self.font.render(eng.QUIT_BUTTON if self.current_lang == 'eng' else rus.QUIT_BUTTON, True, 'yellow')
        self.quit_rect = self.quit_button.get_rect(x=875, y=650)

    def create_elemets_cp(self):
        # Column 1
        self.esc_text = self.font_small.render(eng.MM_ESC if self.current_lang == 'eng' else rus.MM_ESC, False, 'yellow')
        self.esc_text_rect = self.esc_text.get_rect(x=60, y=15)
        self.right_text = self.font_small.render(eng.MM_RIGHT if self.current_lang == 'eng' else rus.MM_RIGHT, False, 'yellow')
        self.right_text_rect = self.right_text.get_rect(x=60, y=55)
        self.left_text = self.font_small.render(eng.MM_LEFT if self.current_lang == 'eng' else rus.MM_LEFT, False, 'yellow')
        self.left_text_rect = self.left_text.get_rect(x=60, y=95)
        self.f5_text = self.font_small.render(eng.MM_F5 if self.current_lang == 'eng' else rus.MM_F5, False, 'yellow')
        self.f5_text_rect = self.f5_text.get_rect(x=60, y=135)
        self.f9_text = self.font_small.render(eng.MM_F9 if self.current_lang == 'eng' else rus.MM_F9, False, 'yellow')
        self.f9_text_rect = self.f9_text.get_rect(x=60, y=175)
        # Column 2
        self.tab_text = self.font_small.render(eng.MM_TAB if self.current_lang == 'eng' else rus.MM_TAB, False, 'yellow')
        self.tab_text_rect = self.tab_text.get_rect(x=360, y=15)
        self.x_text = self.font_small.render(eng.MM_X if self.current_lang == 'eng' else rus.MM_X, False, 'yellow')
        self.x_text_rect = self.x_text.get_rect(x=400, y=55)
        self.down_text = self.font_small.render(eng.MM_DOWN if self.current_lang == 'eng' else rus.MM_DOWN, False, 'yellow')
        self.down_text_rect = self.down_text.get_rect(x=360, y=95)
        self.space_text = self.font_small.render(eng.MM_SPACE if self.current_lang == 'eng' else rus.MM_SPACE, False, 'yellow')
        self.space_text_rect = self.space_text.get_rect(x=530, y=135)

    def create_lang(self):
        self.settings_panel_surf.blit(self.lang_helper, self.lang_helper_rect)
        self.settings_panel_surf.blit(self.eng_lang, self.eng_lang_rect)
        self.settings_panel_surf.blit(self.rus_lang, self.rus_lang_rect)

    # Show section
    def show_buttons(self):
        self.display_surface.blit(self.continie_surf, self.continie_surf_rect)
        self.display_surface.blit(self.new_game_surf, self.new_game_surf_rect)
        self.display_surface.blit(self.controls_surf, self.controls_surf_rect)
        self.display_surface.blit(self.settings_surf, self.settings_surf_rect)
        self.display_surface.blit(self.exit_surf, self.exit_surf_rect)
        self.button_creation()
        self.display_surface.blit(self.main_menu_dct['sc'], self.title_rect)
        self.display_surface.blit(self.continue_button, self.continue_button_rect)
        self.display_surface.blit(self.new_game_button, self.new_game_button_rect)
        self.display_surface.blit(self.controls_button, self.controls_rect)
        self.display_surface.blit(self.settings_button, self.settings_rect)
        self.display_surface.blit(self.quit_button, self.quit_rect)

    def show_controls(self):
        if self.control_panel_is_active:
            self.settings_panel_is_active = False
            self.create_elemets_cp()
            self.control_panel_surf.fill(BLACK_GRAY)
            self.control_panel_surf.blit(self.main_menu_dct['esc'], self.esc_img_rect)
            self.control_panel_surf.blit(self.main_menu_dct['right'], self.right_button_rect)
            self.control_panel_surf.blit(self.main_menu_dct['left'], self.left_button_rect)
            self.control_panel_surf.blit(self.main_menu_dct['f5'], self.save_button_rect)
            self.control_panel_surf.blit(self.main_menu_dct['f9'], self.load_button_rect)
            self.control_panel_surf.blit(self.esc_text, self.esc_text_rect)
            self.control_panel_surf.blit(self.right_text, self.right_text_rect)
            self.control_panel_surf.blit(self.left_text, self.left_text_rect)
            self.control_panel_surf.blit(self.f5_text, self.f5_text_rect)
            self.control_panel_surf.blit(self.f9_text, self.f9_text_rect)
            self.control_panel_surf.blit(self.main_menu_dct['tab'], self.tab_img_rect)
            self.control_panel_surf.blit(self.main_menu_dct['x'], self.x_img_rect)
            self.control_panel_surf.blit(self.main_menu_dct['up'], self.up_img_rect)
            self.control_panel_surf.blit(self.main_menu_dct['down'], self.down_img_rect)
            self.control_panel_surf.blit(self.main_menu_dct['space'], self.space_img_rect)
            self.control_panel_surf.blit(self.tab_text, self.tab_text_rect)
            self.control_panel_surf.blit(self.x_text, self.x_text_rect)
            self.control_panel_surf.blit(self.down_text, self.down_text_rect)
            self.control_panel_surf.blit(self.space_text, self.space_text_rect) 
            self.display_surface.blit(self.control_panel_surf, self.control_panel_surf_rect)
    
    def show_settings(self):
        if self.settings_panel_is_active:
            self.create_lang()
            self.display_surface.blit(self.settings_panel_surf, self.settings_panel_surf_rect)

    def show_current_lang(self):
        if self.settings_panel_is_active:
            match self.current_lang:
                case 'eng':
                    self.change_eng_surf.set_alpha(50)
                    self.change_rus_surf.set_alpha(0)
                case 'rus':
                    self.change_eng_surf.set_alpha(0)
                    self.change_rus_surf.set_alpha(50)
            self.display_surface.blit(self.change_eng_surf, self.change_eng_surf_rect)
            self.display_surface.blit(self.change_rus_surf, self.change_rus_surf_rect)


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
            if event.type == pygame.MOUSEBUTTONDOWN and self.new_game_surf_rect.collidepoint(event.pos):
                self.next_stage = 4
            if event.type == pygame.MOUSEBUTTONDOWN and self.controls_surf_rect.collidepoint(event.pos) and not self.control_panel_is_active:
                self.control_panel_is_active = True
                self.settings_panel_is_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.controls_surf_rect.collidepoint(event.pos) and self.control_panel_is_active:
                self.control_panel_is_active = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.settings_surf_rect.collidepoint(event.pos) and not self.settings_panel_is_active:
                self.settings_panel_is_active = True
                self.control_panel_is_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.settings_surf_rect.collidepoint(event.pos) and self.settings_panel_is_active:
                self.settings_panel_is_active = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.change_eng_surf_rect.collidepoint(event.pos) and self.settings_panel_is_active:
                self.toggle_lang('eng')
            if event.type == pygame.MOUSEBUTTONDOWN and self.change_rus_surf_rect.collidepoint(event.pos) and self.settings_panel_is_active:
                self.toggle_lang('rus')
        
    # Main cycle
    def run(self, dt):
        self.display_surface.fill(BLACK_GRAY)
        self.moving_stars(dt)
        self.moving_moon(dt)
        self.lang_choise()
        self.show_buttons()
        self.show_controls()
        self.show_settings()
        self.show_current_lang()
        
        self.event_loop()
        return 3 if self.next_stage != 4 else 4