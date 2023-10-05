from math import sin
import sys

import pygame


import eng
import rus
from img_imports import import_folder_dict
from settings import *


class MainMenu:
    def __init__(
            self,
            set_prev_stage,
            start_new_game,
            audio,
            config,
            file_path,
            toggle_to_full_screen,
            update_cutscenes,
            transition):

        # main setup
        self.display_surface = pygame.display.get_surface()
        self.prev_stage = 3
        self.set_prev_stage = set_prev_stage
        self.start_new_game = start_new_game
        self.config = config
        self.file_path = file_path
        self.fullscreen_mode = False
        self.toggle_to_full_screen = toggle_to_full_screen
        self.update_curscenes = update_cutscenes
        self.transition = transition

        # Main menu image imports
        self.main_menu_dct = import_folder_dict('images/main_menu/')

        # title and the mansion
        self.title_rect = self.main_menu_dct['sc'].get_rect(
            centerx=WINDOW_WIDTH // 2 + 110, centery=WINDOW_HEIGHT // 2 - 85)

        # Moon
        self.moon_rect = self.main_menu_dct['moon'].get_rect(y=300)
        self.moon_offset = -150
        self.angle = 0

        # sound
        self.bg_music = audio['main_theme']
        self.is_music_playing = False

        # Lang
        self.current_lang = 'eng'

        # Next stage toggle
        self.current_stage = 3

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
        self.control_panel_surf_rect = self.control_panel_surf.get_rect(
            x=50, y=450)
        self.control_panel_is_active = False

        # Controls imports
        # Rectangles for controls
        self.esc_img_rect = self.main_menu_dct['esc'].get_rect(x=10, y=10)
        self.right_button_rect = self.main_menu_dct['right'].get_rect(
            x=10, y=50)
        self.left_button_rect = self.main_menu_dct['left'].get_rect(x=10, y=90)
        self.save_button_rect = self.main_menu_dct['f5'].get_rect(x=10, y=130)
        self.load_button_rect = self.main_menu_dct['f9'].get_rect(x=10, y=170)
        self.tab_img_rect = self.main_menu_dct['tab'].get_rect(x=300, y=10)
        self.x_img_rect = self.main_menu_dct['x'].get_rect(x=300, y=50)
        self.up_img_rect = self.main_menu_dct['up'].get_rect(x=350, y=50)
        self.down_img_rect = self.main_menu_dct['down'].get_rect(x=300, y=90)
        self.space_img_rect = self.main_menu_dct['space'].get_rect(
            x=300, y=130)

        # Settings panel
        self.settings_panel_surf = pygame.Surface((725, 235))
        self.settings_panel_surf.fill(BLACK_GRAY)
        self.settings_panel_surf_rect = self.control_panel_surf.get_rect(
            x=50, y=450)
        self.settings_panel_is_active = False

        # toggle lang
        self.change_eng_surf = pygame.Surface((150, 40))
        self.change_eng_surf_rect = self.change_eng_surf.get_rect(x=70, y=500)
        self.change_eng_surf.fill(MM_BUT_COLOR)

        self.change_rus_surf = pygame.Surface((150, 40))
        self.change_rus_surf_rect = self.change_eng_surf.get_rect(x=230, y=500)
        self.change_rus_surf.fill(MM_BUT_COLOR)

        # Go to Editor Mode
        self.editor_md_surf = pygame.Surface((200, 40))
        self.editor_md_surf_rect = self.editor_md_surf.get_rect(x=70, y=610)
        self.editor_md_surf.fill(MM_BUT_COLOR)

        # Work with Music Sound
        self.music_minus_surf = pygame.Surface((30, 40))
        self.music_minus_rect = self.music_minus_surf.get_rect(x=460, y=500)
        self.music_minus_surf.fill(MM_BUT_COLOR)
        self.sounds_minus_surf = pygame.Surface((30, 40))
        self.sounds_minus_rect = self.sounds_minus_surf.get_rect(x=600, y=500)
        self.sounds_minus_surf.fill(MM_BUT_COLOR)

        # Work with Music Sound
        self.music_plus_surf = pygame.Surface((30, 40))
        self.music_plus_rect = self.music_plus_surf.get_rect(x=545, y=500)
        self.music_plus_surf.fill(MM_BUT_COLOR)
        self.sounds_plus_surf = pygame.Surface((30, 40))
        self.sounds_plus_rect = self.sounds_plus_surf.get_rect(x=694, y=500)
        self.sounds_plus_surf.fill(MM_BUT_COLOR)

        # Fullscreen mode
        self.fscr_surf = pygame.Surface((140, 40))
        self.fscr_rect = self.fscr_surf.get_rect(x=450, y=610)
        self.fscr_surf.fill(MM_BUT_COLOR)

        self.fscr_surf_off = pygame.Surface((140, 40))
        self.fscr_rect_off = self.fscr_surf.get_rect(x=595, y=610)
        self.fscr_surf_off.fill(MM_BUT_COLOR)

        self.lang_helper = self.font_small.render(
            'Click your language / Кликните на ваш язык', False, 'yellow')
        self.eng_lang = self.font.render('English', False, 'yellow')
        self.rus_lang = self.font.render('Русский', False, 'yellow')
        self.lang_helper_rect = self.lang_helper.get_rect(x=30, y=20)
        self.eng_lang_rect = self.eng_lang.get_rect(x=30, y=50)
        self.rus_lang_rect = self.rus_lang.get_rect(x=190, y=50)

    def write_new_lang(self):
        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)

    # Language choice section
    def lang_choise(self):
        self.current_lang = self.config.get('LANG', 'Lang')

    # Start screen section
    def moving_moon(self, dt):
        self.moon_offset += dt * 400
        self.rotated_moon = pygame.transform.rotate(
            self.main_menu_dct['moon'], self.angle)
        self.rotated_moon_rect = self.rotated_moon.get_rect(
            center=(self.moon_rect.x + 50, self.moon_rect.y + 50))
        if -150 <= self.moon_offset <= 1050:
            self.moon_rect.x = int(self.moon_offset)
            self.moon_rect.y = 250 + \
                sin((self.moon_rect.x + 150) * 0.0022) * - 200
            self.display_surface.blit(
                self.main_menu_dct['moon'], self.moon_rect)
        else:
            self.moon_offset = 1051
            self.display_surface.blit(
                self.rotated_moon, self.rotated_moon_rect)
            if self.angle > -5000:
                self.angle -= 0.2
            else:
                self.angle = 0

    def moving_stars(self, dt):
        self.star_offset += dt * 50
        if -150 <= self.star_offset <= 0:
            self.star_rect.x = int(self.star_offset)
            self.display_surface.blit(
                self.main_menu_dct['stars'], self.star_rect)
        else:
            self.display_surface.blit(
                self.main_menu_dct['stars'], self.star_rect)

    # Show section

    def show_buttons(self):
        self.display_surface.blit(self.continie_surf, self.continie_surf_rect)
        self.display_surface.blit(self.new_game_surf, self.new_game_surf_rect)
        self.display_surface.blit(self.controls_surf, self.controls_surf_rect)
        self.display_surface.blit(self.settings_surf, self.settings_surf_rect)
        self.display_surface.blit(self.exit_surf, self.exit_surf_rect)
        self.continue_button = self.font.render(
            eng.CONTINUE_BUTTON if self.current_lang == 'eng' else rus.CONTINUE_BUTTON,
            True,
            'yellow' if self.current_stage != self.prev_stage else 'gray')
        self.continue_button_rect = self.continue_button.get_rect(x=875, y=450)
        self.new_game_button = self.font.render(
            eng.NEW_GAME_BUTTON if self.current_lang == 'eng' else rus.NEW_GAME_BUTTON,
            True,
            'yellow')
        self.new_game_button_rect = self.new_game_button.get_rect(x=875, y=500)
        self.controls_button = self.font.render(
            eng.CONTROLS_BUTTON if self.current_lang == 'eng' else rus.CONTROLS_BUTTON,
            True,
            'yellow')
        self.controls_rect = self.controls_button.get_rect(x=875, y=550)
        self.settings_button = self.font.render(
            eng.SETTINGS_BUTTON if self.current_lang == 'eng' else rus.SETTINGS_BUTTON,
            True,
            'yellow')
        self.settings_rect = self.settings_button.get_rect(x=875, y=600)
        self.quit_button = self.font.render(
            eng.QUIT_BUTTON if self.current_lang == 'eng' else rus.QUIT_BUTTON,
            True,
            'yellow')
        self.quit_rect = self.quit_button.get_rect(x=875, y=650)
        self.display_surface.blit(self.main_menu_dct['sc'], self.title_rect)
        self.display_surface.blit(
            self.continue_button,
            self.continue_button_rect)
        self.display_surface.blit(
            self.new_game_button,
            self.new_game_button_rect)
        self.display_surface.blit(self.controls_button, self.controls_rect)
        self.display_surface.blit(self.settings_button, self.settings_rect)
        self.display_surface.blit(self.quit_button, self.quit_rect)

    def show_controls(self):
        if self.control_panel_is_active:
            self.settings_panel_is_active = False
            self.esc_text = self.font_small.render(
                eng.MM_ESC if self.current_lang == 'eng' else rus.MM_ESC, False, 'yellow')
            self.esc_text_rect = self.esc_text.get_rect(x=60, y=15)
            self.right_text = self.font_small.render(
                eng.MM_RIGHT if self.current_lang == 'eng' else rus.MM_RIGHT, False, 'yellow')
            self.right_text_rect = self.right_text.get_rect(x=60, y=55)
            self.left_text = self.font_small.render(
                eng.MM_LEFT if self.current_lang == 'eng' else rus.MM_LEFT, False, 'yellow')
            self.left_text_rect = self.left_text.get_rect(x=60, y=95)
            self.f5_text = self.font_small.render(
                eng.MM_F5 if self.current_lang == 'eng' else rus.MM_F5, False, 'yellow')
            self.f5_text_rect = self.f5_text.get_rect(x=60, y=135)
            self.f9_text = self.font_small.render(
                eng.MM_F9 if self.current_lang == 'eng' else rus.MM_F9, False, 'yellow')
            self.f9_text_rect = self.f9_text.get_rect(x=60, y=175)
            # Column 2
            self.tab_text = self.font_small.render(
                eng.MM_TAB if self.current_lang == 'eng' else rus.MM_TAB, False, 'yellow')
            self.tab_text_rect = self.tab_text.get_rect(x=360, y=15)
            self.x_text = self.font_small.render(
                eng.MM_X if self.current_lang == 'eng' else rus.MM_X, False, 'yellow')
            self.x_text_rect = self.x_text.get_rect(x=400, y=55)
            self.down_text = self.font_small.render(
                eng.MM_DOWN if self.current_lang == 'eng' else rus.MM_DOWN, False, 'yellow')
            self.down_text_rect = self.down_text.get_rect(x=360, y=95)
            self.space_text = self.font_small.render(
                eng.MM_SPACE if self.current_lang == 'eng' else rus.MM_SPACE, False, 'yellow')
            self.space_text_rect = self.space_text.get_rect(x=530, y=135)
            self.control_panel_surf.fill(BLACK_GRAY)
            self.control_panel_surf.blit(
                self.main_menu_dct['esc'], self.esc_img_rect)
            self.control_panel_surf.blit(
                self.main_menu_dct['right'],
                self.right_button_rect)
            self.control_panel_surf.blit(
                self.main_menu_dct['left'],
                self.left_button_rect)
            self.control_panel_surf.blit(
                self.main_menu_dct['f5'], self.save_button_rect)
            self.control_panel_surf.blit(
                self.main_menu_dct['f9'], self.load_button_rect)
            self.control_panel_surf.blit(self.esc_text, self.esc_text_rect)
            self.control_panel_surf.blit(self.right_text, self.right_text_rect)
            self.control_panel_surf.blit(self.left_text, self.left_text_rect)
            self.control_panel_surf.blit(self.f5_text, self.f5_text_rect)
            self.control_panel_surf.blit(self.f9_text, self.f9_text_rect)
            self.control_panel_surf.blit(
                self.main_menu_dct['tab'], self.tab_img_rect)
            self.control_panel_surf.blit(
                self.main_menu_dct['x'], self.x_img_rect)
            self.control_panel_surf.blit(
                self.main_menu_dct['up'], self.up_img_rect)
            self.control_panel_surf.blit(
                self.main_menu_dct['down'], self.down_img_rect)
            self.control_panel_surf.blit(
                self.main_menu_dct['space'], self.space_img_rect)
            self.control_panel_surf.blit(self.tab_text, self.tab_text_rect)
            self.control_panel_surf.blit(self.x_text, self.x_text_rect)
            self.control_panel_surf.blit(self.down_text, self.down_text_rect)
            self.control_panel_surf.blit(self.space_text, self.space_text_rect)
            self.display_surface.blit(
                self.control_panel_surf,
                self.control_panel_surf_rect)

    def show_settings(self):
        if self.settings_panel_is_active:
            self.settings_panel_surf.blit(
                self.lang_helper, self.lang_helper_rect)
            self.settings_panel_surf.blit(self.eng_lang, self.eng_lang_rect)
            self.settings_panel_surf.blit(self.rus_lang, self.rus_lang_rect)
            self.editor_mode = self.font_small.render(
                eng.ED_MD if self.current_lang == 'eng' else rus.ED_MD, False, 'yellow')
            self.editor_mode_rect = self.editor_mode.get_rect(x=30, y=130)
            self.go_editor = self.font_small.render(
                eng.GO_TO_ED if self.current_lang == 'eng' else rus.GO_TO_ED, False, 'yellow')
            self.go_editor_rect = self.editor_mode.get_rect(x=30, y=170)
            self.volume_settings = self.font_small.render(
                eng.MM_VOLUME if self.current_lang == 'eng' else rus.MM_VOLUME, False, 'yellow')
            self.volume_settings_rect = self.volume_settings.get_rect(
                x=410, y=20)
            self.full_screen = self.font_small.render(
                eng.MM_FULLSCREEN if self.current_lang == 'eng' else rus.MM_FULLSCREEN,
                False,
                'yellow')
            self.full_screen_rect = self.full_screen.get_rect(x=410, y=130)

            self.fscr_on = self.font.render(
                eng.MM_FLSC_ON if self.current_lang == 'eng' else rus.MM_FLSC_ON, True, 'yellow')
            self.fscr_off = self.font.render(
                eng.MM_FLSC_OFF if self.current_lang == 'eng' else rus.MM_FLSC_OFF,
                True,
                'yellow')
            self.fscr_on_rect = self.fscr_on.get_rect(x=410, y=160)
            self.fscr_off_rect = self.fscr_off.get_rect(x=550, y=160)

            # Contol Volume's value
            self.get_minus = self.font.render('-', True, 'yellow')
            self.get_minus_rect = self.get_minus.get_rect(x=420, y=50)
            self.get_minus_rect_1 = self.get_minus.get_rect(x=560, y=50)

            self.get_plus = self.font.render('+', True, 'yellow')
            self.get_plus_rect = self.get_plus.get_rect(x=500, y=50)
            self.get_plus_rect_1 = self.get_plus.get_rect(x=650, y=50)

            self.show_music_volume = self.font.render(
                self.config['SOUNDS']['music'], True, 'yellow')
            self.show_sounds_volume = self.font.render(
                self.config['SOUNDS']['sounds'], True, 'yellow')
            self.show_music_volume_rect = self.show_music_volume.get_rect(
                x=450, y=50)
            self.show_sounds_volume_rect = self.show_sounds_volume.get_rect(
                x=590, y=50)

            self.frame_1 = pygame.draw.rect(
                self.settings_panel_surf, MM_BUT_COLOR, (10, 10, 375, 90), 3)
            self.frame_2 = pygame.draw.rect(
                self.settings_panel_surf, MM_BUT_COLOR, (10, 120, 375, 90), 3)
            self.frame_3 = pygame.draw.rect(
                self.settings_panel_surf, MM_BUT_COLOR, (400, 10, 310, 90), 3)
            self.frame_4 = pygame.draw.rect(
                self.settings_panel_surf, MM_BUT_COLOR, (400, 120, 310, 90), 3)
            self.settings_panel_surf.blit(
                self.editor_mode, self.editor_mode_rect)
            self.settings_panel_surf.blit(self.go_editor, self.go_editor_rect)
            self.settings_panel_surf.blit(
                self.volume_settings, self.volume_settings_rect)
            self.settings_panel_surf.blit(
                self.full_screen, self.full_screen_rect)
            self.settings_panel_surf.blit(self.fscr_on, self.fscr_on_rect)
            self.settings_panel_surf.blit(self.fscr_off, self.fscr_off_rect)
            self.settings_panel_surf.blit(self.get_minus, self.get_minus_rect)
            self.settings_panel_surf.blit(
                self.get_minus, self.get_minus_rect_1)
            self.settings_panel_surf.blit(
                self.show_music_volume,
                self.show_music_volume_rect)
            self.settings_panel_surf.blit(
                self.show_sounds_volume,
                self.show_sounds_volume_rect)
            self.settings_panel_surf.blit(self.get_plus, self.get_plus_rect)
            self.settings_panel_surf.blit(self.get_plus, self.get_plus_rect_1)
            self.display_surface.blit(
                self.settings_panel_surf,
                self.settings_panel_surf_rect)
            self.settings_panel_surf.fill(BLACK_GRAY)

        if self.settings_panel_is_active:
            match self.current_lang:
                case 'eng':
                    self.change_eng_surf.set_alpha(50)
                    self.change_rus_surf.set_alpha(0)
                case 'rus':
                    self.change_eng_surf.set_alpha(0)
                    self.change_rus_surf.set_alpha(50)
            if self.config.getboolean('FULLSCREEN', 'fullscreen'):
                self.fscr_surf.set_alpha(50)
                self.fscr_surf_off.set_alpha(0)
            else:
                self.fscr_surf.set_alpha(0)
                self.fscr_surf_off.set_alpha(50)
            self.display_surface.blit(
                self.change_eng_surf,
                self.change_eng_surf_rect)
            self.display_surface.blit(
                self.change_rus_surf,
                self.change_rus_surf_rect)
            self.editor_md_surf.set_alpha(50)
            self.music_minus_surf.set_alpha(50)
            self.sounds_minus_surf.set_alpha(50)
            self.music_plus_surf.set_alpha(50)
            self.sounds_plus_surf.set_alpha(50)

            # Show button '-'
            self.display_surface.blit(
                self.music_minus_surf, self.music_minus_rect)
            self.display_surface.blit(
                self.sounds_minus_surf,
                self.sounds_minus_rect)

            # Show button '+'
            self.display_surface.blit(
                self.music_plus_surf, self.music_plus_rect)
            self.display_surface.blit(
                self.sounds_plus_surf, self.sounds_plus_rect)

            # Show fullscreen surfaces
            self.display_surface.blit(self.fscr_surf, self.fscr_rect)
            self.display_surface.blit(self.fscr_surf_off, self.fscr_rect_off)

            self.display_surface.blit(
                self.editor_md_surf, self.editor_md_surf_rect)

    def change_volume(self, volume_type, minus):
        current_music_volume = float(self.config['SOUNDS']['music'])
        current_sounds_volume = float(self.config['SOUNDS']['sounds'])
        match volume_type:
            case 'music':
                if minus:
                    current_music_volume -= 0.1 if 0.0 < current_music_volume <= 1.0 else 0
                    self.config['SOUNDS']['music'] = str(
                        round(current_music_volume, 1))
                else:
                    current_music_volume += 0.1 if 0.0 <= current_music_volume < 1.0 else 0
                    self.config['SOUNDS']['music'] = str(
                        round(current_music_volume, 1))
            case 'sounds':
                if minus:
                    current_sounds_volume -= 0.1 if 0.0 < current_sounds_volume <= 1.0 else 0
                    self.config['SOUNDS']['sounds'] = str(
                        round(current_sounds_volume, 1))
                else:
                    current_sounds_volume += 0.1 if 0.0 <= current_sounds_volume < 1.0 else 0
                    self.config['SOUNDS']['sounds'] = str(
                        round(current_sounds_volume, 1))

        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)

        self.bg_music.stop()
        self.is_music_playing = False

    def play_sound(self):
        if not self.is_music_playing:
            self.bg_music.set_volume(float(self.config['SOUNDS']['music']))
            self.bg_music.play(loops=-1)
            self.is_music_playing = True

    def rewrite_config_fullscreen(self):
        if self.fullscreen_mode:
            self.config['FULLSCREEN']['fullscreen'] = 'True'
        else:
            self.config['FULLSCREEN']['fullscreen'] = 'False'
        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)

    # Event section
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                self.continie_surf.fill(MM_BUT_COLOR) if self.continie_surf_rect.collidepoint(
                    event.pos) and self.continue_button.get_at(
                    (0, 0)) == (
                    255, 255, 0, 0) else self.continie_surf.fill(BLACK_GRAY)
                self.new_game_surf.fill(MM_BUT_COLOR) if self.new_game_surf_rect.collidepoint(
                    event.pos) else self.new_game_surf.fill(BLACK_GRAY)
                self.controls_surf.fill(MM_BUT_COLOR) if self.controls_surf_rect.collidepoint(
                    event.pos) else self.controls_surf.fill(BLACK_GRAY)
                self.settings_surf.fill(MM_BUT_COLOR) if self.settings_surf_rect.collidepoint(
                    event.pos) else self.settings_surf.fill(BLACK_GRAY)
                self.exit_surf.fill(MM_BUT_COLOR) if self.exit_surf_rect.collidepoint(
                    event.pos) else self.exit_surf.fill(BLACK_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN and self.exit_surf_rect.collidepoint(
                    event.pos):
                pygame.quit()
                sys.exit()
            if self.prev_stage != self.current_stage and event.type == pygame.MOUSEBUTTONDOWN and self.continie_surf_rect.collidepoint(
                    event.pos):
                self.bg_music.stop()
                self.set_prev_stage(self.current_stage, self.prev_stage)
                self.current_stage = self.prev_stage
                self.is_music_playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.new_game_surf_rect.collidepoint(
                    event.pos):
                self.bg_music.stop()
                self.start_new_game()
                self.transition()
                self.current_stage = 'CS1'
                self.is_music_playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.controls_surf_rect.collidepoint(
                    event.pos) and not self.control_panel_is_active:
                self.control_panel_is_active = True
                self.settings_panel_is_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.controls_surf_rect.collidepoint(event.pos) and self.control_panel_is_active:
                self.control_panel_is_active = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.settings_surf_rect.collidepoint(
                    event.pos) and not self.settings_panel_is_active:
                self.settings_panel_is_active = True
                self.control_panel_is_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.settings_surf_rect.collidepoint(event.pos) and self.settings_panel_is_active:
                self.settings_panel_is_active = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.change_eng_surf_rect.collidepoint(
                    event.pos) and self.settings_panel_is_active:
                self.config['LANG']['Lang'] = 'eng'
                self.update_curscenes()
                self.write_new_lang()
            if event.type == pygame.MOUSEBUTTONDOWN and self.change_rus_surf_rect.collidepoint(
                    event.pos) and self.settings_panel_is_active:
                self.config['LANG']['Lang'] = 'rus'
                self.update_curscenes()
                self.write_new_lang()
            if event.type == pygame.MOUSEBUTTONDOWN and self.editor_md_surf_rect.collidepoint(
                    event.pos) and self.settings_panel_is_active:
                self.bg_music.stop()
                self.current_stage = 0
                self.is_music_playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.music_minus_rect.collidepoint(
                    event.pos) and self.settings_panel_is_active:
                self.change_volume(volume_type='music', minus=True)
                self.is_music_playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.music_plus_rect.collidepoint(
                    event.pos) and self.settings_panel_is_active:
                self.change_volume(volume_type='music', minus=False)
                self.is_music_playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.sounds_minus_rect.collidepoint(
                    event.pos) and self.settings_panel_is_active:
                self.change_volume(volume_type='sounds', minus=True)
                self.is_music_playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.sounds_plus_rect.collidepoint(
                    event.pos) and self.settings_panel_is_active:
                self.change_volume(volume_type='sounds', minus=False)
            if event.type == pygame.MOUSEBUTTONDOWN and self.fscr_rect.collidepoint(
                    event.pos) and self.settings_panel_is_active:
                self.fullscreen_mode = True
                self.rewrite_config_fullscreen()
                self.toggle_to_full_screen()
            if event.type == pygame.MOUSEBUTTONDOWN and self.fscr_rect_off.collidepoint(
                    event.pos) and self.settings_panel_is_active:
                self.fullscreen_mode = False
                self.rewrite_config_fullscreen()
                self.toggle_to_full_screen()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.current_stage != self.prev_stage:
                self.bg_music.stop()
                self.set_prev_stage(self.current_stage, self.prev_stage)
                self.current_stage = self.prev_stage
                self.is_music_playing = False

    # Main cycle
    def run(self, dt, current_stage, prev_stage):
        pygame.mouse.set_visible(True)
        self.current_stage = current_stage
        self.prev_stage = prev_stage

        self.display_surface.fill(BLACK_GRAY)
        self.play_sound()
        self.moving_stars(dt)
        self.moving_moon(dt)
        self.lang_choise()
        self.show_buttons()
        self.show_controls()
        self.show_settings()

        self.event_loop()
        return self.current_stage
